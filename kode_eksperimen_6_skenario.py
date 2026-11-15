# kode_eksperimen_6_skenario.py
# -*- coding: utf-8 -*-
"""
Skrip Eksperimen 6 Skenario:
Membandingkan 3 Model x Variasi Eksogen (Tanpa Eksogen, Eksogen t, Eksogen t-1 / Lag-1)
pada 190 unit armada alat berat.
Menghasilkan metrik MAPE dan RMSE per unit serta tabel ringkasan komparasi.
"""

import warnings
warnings.filterwarnings('ignore')
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from statsmodels.tsa.arima.model import ARIMA
import sys

# Menggunakan path relatif
BASE_DIR = Path(__file__).resolve().parent if '__file__' in globals() else Path('.')
sys.path.insert(0, str(BASE_DIR))
import pipeline_lib as pl

def calc_mape(actual, pred):
    """Menghitung Mean Absolute Percentage Error (%)."""
    actual = np.asarray(actual, dtype=float)
    pred = np.asarray(pred, dtype=float)
    mask = actual > 0
    if not np.any(mask):
        return np.nan
    return float(np.mean(np.abs((actual[mask] - pred[mask]) / actual[mask])) * 100)

def calc_rmse(actual, pred):
    """Menghitung Root Mean Square Error (jam)."""
    actual = np.asarray(actual, dtype=float)
    pred = np.asarray(pred, dtype=float)
    return float(np.sqrt(np.mean((actual - pred) ** 2)))

def run_experiment_6_skenario(output_dir=None):
    """Menjalankan evaluasi 6 skenario dan menyimpan hasilnya ke perbandingan_eksogen_dan_model.xlsx."""
    if output_dir is None:
        out_dir = Path('./checkpoints_v4/rev_h3')
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ckpt_base = Path('./checkpoints_v4')
    h3_dir = ckpt_base / 'h3bulan'
    
    # 1. Load dataset monthly_full dan final config 190 unit
    monthly_full = pl.load_monthly_full_checkpoint(ckpt_base)
    
    # Mapping unit baru (K##_UNIT_###) jika ada
    ref_candidates = [
        out_dir / 'mapping_unit_dan_kriteria.xlsx',
        ckpt_base / 'rev_h3' / 'mapping_unit_dan_kriteria.xlsx',
        ckpt_base / 'mapping_unit_dan_kriteria.xlsx',
    ]
    ref_path = next((p for p in ref_candidates if p.exists()), None)
    if ref_path is not None:
        try:
            df_ref = pd.read_excel(ref_path, sheet_name='Mapping_Unit')
            old_to_k_unit = dict(zip(df_ref['EQUIP_NAME_LAMA'], df_ref['EQUIP_NAME_BARU']))
            monthly_full['EQUIP NAME'] = monthly_full['EQUIP NAME'].map(lambda u: old_to_k_unit.get(u, u))
        except Exception:
            pass

    # Ambil 190 unit valid dari checkpoint
    cfg_190_path = out_dir / 'forcedgb_vs_v2b_comparison_190unit.xlsx'
    if not cfg_190_path.exists():
        cfg_190_path = ckpt_base / 'rev_h3' / 'forcedgb_vs_v2b_comparison_190unit.xlsx'
        
    if cfg_190_path.exists():
        final_u = pd.read_excel(cfg_190_path, sheet_name='Per_Unit')
    else:
        final_u = pl.load_final_config(h3_dir, level='unit')

    # 2. Siapkan fitur eksogen lag-1 (t-1)
    exog = monthly_full.groupby('TAHUN_BULAN')[['CURAH_HUJAN', 'VOLUME_CONTAINER']].first().sort_index()
    exog['CH_LAG1'] = exog['CURAH_HUJAN'].shift(1).bfill()
    exog['VC_LAG1'] = exog['VOLUME_CONTAINER'].shift(1).bfill()
    monthly_full = monthly_full.merge(exog[['CH_LAG1', 'VC_LAG1']], on='TAHUN_BULAN', how='left')

    # 3. Split train dan test
    train_raw = monthly_full[monthly_full['TAHUN_BULAN'] <= pl.TRAIN_END].copy()
    test_raw = monthly_full[(monthly_full['TAHUN_BULAN'] >= pl.TEST_START) & (monthly_full['TAHUN_BULAN'] <= pl.TEST_END)].copy()

    arimax_orders = {
        'baseline': (2, 1, 0),
        'robust': (2, 0, 0),
        'savgol': (1, 0, 0),
        'yeojohnson': (2, 0, 0),
    }

    print(f"[Eksperimen 6 Skenario] Memproses evaluasi {len(final_u)} unit analisis...")

    results = []
    feat_base = [f"lag_{i}" for i in range(1, pl.N_LAGS + 1)]
    feat_cur = feat_base + ['CURAH_HUJAN', 'VOLUME_CONTAINER']
    feat_lag1 = feat_base + ['CH_LAG1', 'VC_LAG1']

    for idx, (_, row) in enumerate(final_u.iterrows()):
        unit = row['EQUIP NAME']
        variant = row['V4_GB_VARIAN']
        params = pl.clean_gb_params(row)

        prep_fn = pl.DATA_PREP_VARIANTS[variant]
        u_train = train_raw[train_raw['EQUIP NAME'] == unit].sort_values('TAHUN_BULAN')
        u_test = test_raw[test_raw['EQUIP NAME'] == unit].sort_values('TAHUN_BULAN')

        tr_p, te_p, tf = prep_fn(u_train, u_test)
        full_p = pd.concat([tr_p, te_p], ignore_index=True).sort_values('TAHUN_BULAN')

        for lag in range(1, pl.N_LAGS + 1):
            full_p[f"lag_{lag}"] = full_p['UTILITAS_SMOOTH'].shift(lag)

        tr_lag = full_p[full_p['TAHUN_BULAN'] <= pl.TRAIN_END].dropna(subset=[f"lag_{i}" for i in range(1, pl.N_LAGS + 1)] + ['UTILITAS_SMOOTH'])
        te_lag = full_p[(full_p['TAHUN_BULAN'] >= pl.TEST_START) & (full_p['TAHUN_BULAN'] <= pl.TEST_END)]

        col_target_test = 'OPERATING_HOURS' if 'OPERATING_HOURS' in u_test.columns else 'UTILITAS'
        actual_test = u_test.set_index('TAHUN_BULAN')[col_target_test].reindex(te_lag['TAHUN_BULAN']).values

        if len(tr_lag) < 6 or len(te_lag) == 0:
            continue

        # --- GB-1: Eksogen t ---
        m_gb_cur = HistGradientBoostingRegressor(random_state=42, **params)
        m_gb_cur.fit(tr_lag[feat_cur], tr_lag['UTILITAS_SMOOTH'])
        pred_gb_cur = pl.inverse_transform_pred(m_gb_cur.predict(te_lag[feat_cur]), unit, tf)
        mape_gb_cur = calc_mape(actual_test, pred_gb_cur)
        rmse_gb_cur = calc_rmse(actual_test, pred_gb_cur)

        # --- GB-2: Eksogen Lag-1 (t-1) ---
        m_gb_lag1 = HistGradientBoostingRegressor(random_state=42, **params)
        m_gb_lag1.fit(tr_lag[feat_lag1], tr_lag['UTILITAS_SMOOTH'])
        pred_gb_lag1 = pl.inverse_transform_pred(m_gb_lag1.predict(te_lag[feat_lag1]), unit, tf)
        mape_gb_lag1 = calc_mape(actual_test, pred_gb_lag1)
        rmse_gb_lag1 = calc_rmse(actual_test, pred_gb_lag1)

        # --- GB-3: Tanpa Eksogen ---
        m_gb_no = HistGradientBoostingRegressor(random_state=42, **params)
        m_gb_no.fit(tr_lag[feat_base], tr_lag['UTILITAS_SMOOTH'])
        pred_gb_no = pl.inverse_transform_pred(m_gb_no.predict(te_lag[feat_base]), unit, tf)
        mape_gb_no = calc_mape(actual_test, pred_gb_no)
        rmse_gb_no = calc_rmse(actual_test, pred_gb_no)

        # --- ARIMA Models ---
        order = arimax_orders.get(variant, (2, 1, 0))
        y_tr = tr_p['UTILITAS_SMOOTH'].values
        n_te = len(te_p)

        # ARIMA Murni
        try:
            ar_no = ARIMA(y_tr, order=order).fit()
            p_ar_no = pl.inverse_transform_pred(ar_no.forecast(steps=n_te), unit, tf)
            mape_ar_no = calc_mape(actual_test, p_ar_no)
            rmse_ar_no = calc_rmse(actual_test, p_ar_no)
        except Exception:
            mape_ar_no, rmse_ar_no = np.nan, np.nan

        # ARIMAX Eksogen t
        try:
            x_tr_cur = tr_p[['CURAH_HUJAN', 'VOLUME_CONTAINER']].values
            x_te_cur = te_p[['CURAH_HUJAN', 'VOLUME_CONTAINER']].values
            ar_cur = ARIMA(y_tr, order=order, exog=x_tr_cur).fit()
            p_ar_cur = pl.inverse_transform_pred(ar_cur.forecast(steps=n_te, exog=x_te_cur), unit, tf)
            mape_ar_cur = calc_mape(actual_test, p_ar_cur)
            rmse_ar_cur = calc_rmse(actual_test, p_ar_cur)
        except Exception:
            mape_ar_cur, rmse_ar_cur = np.nan, np.nan

        # ARIMAX Eksogen Lag-1
        try:
            x_tr_lag1 = tr_p[['CH_LAG1', 'VC_LAG1']].values
            x_te_lag1 = te_p[['CH_LAG1', 'VC_LAG1']].values
            ar_lag1 = ARIMA(y_tr, order=order, exog=x_tr_lag1).fit()
            p_ar_lag1 = pl.inverse_transform_pred(ar_lag1.forecast(steps=n_te, exog=x_te_lag1), unit, tf)
            mape_ar_lag1 = calc_mape(actual_test, p_ar_lag1)
            rmse_ar_lag1 = calc_rmse(actual_test, p_ar_lag1)
        except Exception:
            mape_ar_lag1, rmse_ar_lag1 = np.nan, np.nan

        results.append({
            'EQUIP NAME': unit,
            'VARIAN': variant,
            'MAPE_GB_EXOG_T': mape_gb_cur,
            'RMSE_GB_EXOG_T': rmse_gb_cur,
            'MAPE_GB_EXOG_LAG1': mape_gb_lag1,
            'RMSE_GB_EXOG_LAG1': rmse_gb_lag1,
            'MAPE_GB_NO_EXOG': mape_gb_no,
            'RMSE_GB_NO_EXOG': rmse_gb_no,
            'MAPE_ARIMA_NO_EXOG': mape_ar_no,
            'RMSE_ARIMA_NO_EXOG': rmse_ar_no,
            'MAPE_ARIMAX_EXOG_T': mape_ar_cur,
            'RMSE_ARIMAX_EXOG_T': rmse_ar_cur,
            'MAPE_ARIMAX_EXOG_LAG1': mape_ar_lag1,
            'RMSE_ARIMAX_EXOG_LAG1': rmse_ar_lag1,
        })

    res_df = pd.DataFrame(results)

    # 4. Buat Tabel Ringkasan
    skenario_defs = [
        ('Gradient Boosting (Eksogen t)', 'MAPE_GB_EXOG_T', 'RMSE_GB_EXOG_T'),
        ('Gradient Boosting (Eksogen Lag-1 / t-1)', 'MAPE_GB_EXOG_LAG1', 'RMSE_GB_EXOG_LAG1'),
        ('Gradient Boosting (Tanpa Eksogen)', 'MAPE_GB_NO_EXOG', 'RMSE_GB_NO_EXOG'),
        ('ARIMA Murni (Tanpa Eksogen)', 'MAPE_ARIMA_NO_EXOG', 'RMSE_ARIMA_NO_EXOG'),
        ('ARIMAX (Eksogen t)', 'MAPE_ARIMAX_EXOG_T', 'RMSE_ARIMAX_EXOG_T'),
        ('ARIMAX (Eksogen Lag-1 / t-1)', 'MAPE_ARIMAX_EXOG_LAG1', 'RMSE_ARIMAX_EXOG_LAG1'),
    ]

    ringkasan_rows = []
    for label, m_col, r_col in skenario_defs:
        s_m = res_df[m_col].dropna()
        s_r = res_df[r_col].dropna()
        ringkasan_rows.append({
            'Model & Skenario': label,
            'Mean MAPE (%)': float(s_m.mean()),
            'Median MAPE (%)': float(s_m.median()),
            'Max MAPE (%)': float(s_m.max()),
            'Mean RMSE': float(s_r.mean()),
        })

    ringkasan_df = pd.DataFrame(ringkasan_rows)

    # 5. Simpan ke Excel perbandingan_eksogen_dan_model.xlsx
    excel_out = out_dir / 'perbandingan_eksogen_dan_model.xlsx'
    with pd.ExcelWriter(excel_out, engine='openpyxl') as writer:
        ringkasan_df.to_excel(writer, sheet_name='Ringkasan', index=False)
        res_df.to_excel(writer, sheet_name='Detail_PerUnit', index=False)

    print(f"\n[Eksperimen 6 Skenario] Berhasil disimpan ke: {excel_out}")
    print("\n=== RINGKASAN HASIL EVALUASI 190 UNIT ANALISIS ===")
    print(ringkasan_df.round(2).to_string(index=False))
    return ringkasan_df

if __name__ == '__main__':
    run_experiment_6_skenario()

