# -*- coding: utf-8 -*-
"""
appDemo.py -- Dashboard DEMO (sidang)
======================================
Menampilkan semua hasil yang sudah dikerjakan: perbandingan GB Seragam vs Model Terbaik
per unit/kriteria (hasil Tahap 2b/Force-GB), MAPE/RMSE, plot training vs testing, dan plot
actual sampai future forecast (horizon fleksibel 3-12 bulan, default 3).

Jalankan: streamlit run appDemo.py
Catatan: dashboard ini BACA hasil yang sudah ada di ./checkpoints_v4 (hasil code_v4.ipynb
Tahap 1-3). Kalau belum pernah dijalankan sampai Tahap 3, jalankan notebook dulu.
"""

import importlib
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import pipeline_lib as pl
importlib.reload(pl)

st.set_page_config(page_title="Demo Prediksi Operating Hours Alat Berat", layout="wide")

BASE_DIR = Path("./checkpoints_v4")
H3_DIR = (BASE_DIR / "rev_h3") if (BASE_DIR / "rev_h3").exists() else (BASE_DIR / "h3bulan")


# ---------------------------------------------------------------------------
# Loader (di-cache supaya gak baca ulang file tiap klik)
# ---------------------------------------------------------------------------
@st.cache_data
def load_all(_v=3):
    data = {}
    data["monthly_full"] = pl.load_monthly_full_checkpoint(BASE_DIR)
    data["final_unit"] = pl.load_final_config(H3_DIR, level="unit")
    valid_units = set(data["final_unit"]["EQUIP NAME"].unique())

    krit_all = pl.load_kriteria_checkpoint(BASE_DIR)
    data["kriteria"] = krit_all[krit_all["EQUIP NAME"].isin(valid_units)].reset_index(drop=True)

    final_krit = pl.load_final_config(H3_DIR, level="kriteria")
    active_krit = set(data["kriteria"]["KRITERIA_ID"].unique())
    data["final_krit"] = final_krit[final_krit["KRITERIA_ID"].isin(active_krit)].reset_index(drop=True)

    rolling_unit = pl.load_rolling_vs_direct(H3_DIR, level="unit")
    data["rolling_unit"] = rolling_unit[rolling_unit["EQUIP NAME"].isin(valid_units)].reset_index(drop=True)

    rolling_krit = pl.load_rolling_vs_direct(H3_DIR, level="kriteria")
    data["rolling_krit"] = rolling_krit[rolling_krit["KRITERIA_ID"].isin(active_krit)].reset_index(drop=True)

    data["excluded"] = pl.load_excluded_summary(H3_DIR)
    fc = pl.load_future_forecast(H3_DIR)
    data["future_forecast"] = fc[fc["EQUIP NAME"].isin(valid_units)].reset_index(drop=True)
    data["future_forecast"]["TAHUN_BULAN"] = pd.PeriodIndex(data["future_forecast"]["TAHUN_BULAN"], freq="M")

    v2b_u12 = pl.load_v2b_12kombinasi(H3_DIR, level="unit")
    data["v2b_unit_12"] = v2b_u12[v2b_u12["EQUIP NAME"].isin(valid_units)].reset_index(drop=True)

    v2b_uraw = pl.load_v2b_raw_preds(H3_DIR, level="unit")
    data["v2b_unit_raw"] = v2b_uraw[v2b_uraw["EQUIP NAME"].isin(valid_units)].reset_index(drop=True)

    v2b_k12 = pl.load_v2b_12kombinasi(H3_DIR, level="kriteria")
    data["v2b_krit_12"] = v2b_k12[v2b_k12["KRITERIA_ID"].isin(active_krit)].reset_index(drop=True)

    v2b_kraw = pl.load_v2b_raw_preds(H3_DIR, level="kriteria")
    data["v2b_krit_raw"] = v2b_kraw[v2b_kraw["KRITERIA_ID"].isin(active_krit)].reset_index(drop=True)

    try:
        data["kriteria_mapping"] = pl.load_kriteria_mapping(BASE_DIR)
    except FileNotFoundError:
        data["kriteria_mapping"] = None
    return data


try:
    DATA = load_all()
except FileNotFoundError as e:
    st.error(
        "Belum ada data model yang lengkap di ./checkpoints_v4. "
        "Pastikan proses pemodelan telah selesai dijalankan sebelum membuka dashboard ini.\n\n"
        f"Detail: {e}"
    )
    st.stop()


@st.cache_data
def eval_unit_on_test_cached(unit_name, _v=2):
    row = DATA["final_unit"][DATA["final_unit"]["EQUIP NAME"] == unit_name].iloc[0]
    return pl.evaluate_unit_on_test(DATA["monthly_full"], row)


@st.cache_data
def eval_kriteria_on_test_cached(krit_id, _v=2):
    row = DATA["final_krit"][DATA["final_krit"]["KRITERIA_ID"] == krit_id].iloc[0]
    return pl.evaluate_kriteria_on_test(DATA["monthly_full"], DATA["kriteria"], row)


@st.cache_data
def retrain_forecast_kriteria_cached(krit_id, horizon, _v=2):
    exog_future = pl.estimate_future_exog(DATA["monthly_full"], horizon=horizon)
    row = DATA["final_krit"][DATA["final_krit"]["KRITERIA_ID"] == krit_id].iloc[0]
    total, per_unit = pl.retrain_and_forecast_kriteria(
        DATA["monthly_full"], DATA["kriteria"], row, exog_future, horizon=horizon
    )
    return total, per_unit


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("Pengaturan")
tampilan = st.sidebar.radio("Tampilan", ["Per Unit", "Per Kriteria"])
horizon = st.sidebar.slider("Horizon forecast ke depan (bulan)", min_value=3, max_value=12, value=3)
if horizon > 3:
    st.sidebar.warning(
        "Horizon di atas 3 bulan dipakai di luar skenario evaluasi utama (train/test 3 bulan). "
        "Forecast masa depan juga wajib pakai pendekatan rolling (bukan direct), jadi makin jauh "
        "horizon, potensi error makin besar."
    )

st.title("Demo Sistem Prediksi Operating Hours Alat Berat")
st.caption("Horizon final: 3 bulan, per unit, Gradient Boosting (data-prep & hyperparameter individual per unit)")

tab_overview, tab_detail, tab_rolling = st.tabs(["Ringkasan", "Detail per Unit/Kriteria", "Rolling vs Direct"])

# ---------------------------------------------------------------------------
# TAB: Ringkasan
# ---------------------------------------------------------------------------
with tab_overview:
    df_ref = DATA["final_unit"] if tampilan == "Per Unit" else DATA["final_krit"]
    key_col = "EQUIP NAME" if tampilan == "Per Unit" else "KRITERIA_ID"

    c1, c2, c3 = st.columns(3)
    c1.metric("Jumlah " + ("unit" if tampilan == "Per Unit" else "kriteria"), df_ref[key_col].nunique())
    c2.metric("Rata-rata MAPE (Gradient Boosting)", f'{df_ref["V4_GB_MAPE"].mean():.2f}%')
    c3.metric("Rata-rata MAPE (Model Alternatif Terbaik)", f'{df_ref["V2B_BEST_MAPE"].mean():.2f}%')

    st.subheader("Perbandingan Performa: Gradient Boosting vs Model Alternatif")
    show_cols = [key_col, "V4_GB_VARIAN", "V4_GB_MAPE", "V4_GB_RMSE",
                 "V2B_BEST_MODEL", "V2B_BEST_VARIAN", "V2B_BEST_MAPE", "V2B_BEST_RMSE", "SELISIH_MAPE_GBvsV2B"]
    show_cols = [c for c in show_cols if c in df_ref.columns]
    rename_cols = {
        "EQUIP NAME": "Nama Unit",
        "KRITERIA_ID": "Kriteria ID",
        "V4_GB_VARIAN": "Varian GB",
        "V4_GB_MAPE": "MAPE GB (%)",
        "V4_GB_RMSE": "RMSE GB",
        "V2B_BEST_MODEL": "Model Alternatif",
        "V2B_BEST_VARIAN": "Varian Alternatif",
        "V2B_BEST_MAPE": "MAPE Alternatif (%)",
        "V2B_BEST_RMSE": "RMSE Alternatif",
        "SELISIH_MAPE_GBvsV2B": "Selisih MAPE (%)",
    }
    st.dataframe(df_ref[show_cols].sort_values(key_col).rename(columns=rename_cols), use_container_width=True, height=400)

    st.subheader("Daftar Unit yang Diexclude beserta Alasan")
    df_excluded = DATA["excluded"].copy()
    reason_map = {
        "nol total di salah satu tahun train": "Data operating hours pada salah satu tahun periode data train bernilai nol semua",
        "Nol total di salah satu tahun train": "Data operating hours pada salah satu tahun periode data train bernilai nol semua",
        "test bernilai nol seluruhnya": "Data operating hours pada periode data test bernilai nol semua",
        "Test bernilai nol seluruhnya": "Data operating hours pada periode data test bernilai nol semua",
    }
    if "ALASAN" in df_excluded.columns:
        df_excluded = df_excluded[~df_excluded["ALASAN"].astype(str).str.contains("review MAPE|data baru|threshold|toleransi", case=False, na=False)]
        df_excluded["ALASAN"] = (
            df_excluded["ALASAN"].astype(str).str.strip()
            .map(lambda s: reason_map.get(s, s[0].upper() + s[1:] if len(s) > 0 else s))
            .str.replace("utilitas", "operating hours", case=False)
        )
    df_excluded_display = df_excluded[["EQUIP NAME", "ALASAN"]].rename(columns={
        "EQUIP NAME": "Nama Unit",
        "ALASAN": "Alasan",
    })
    st.dataframe(df_excluded_display, use_container_width=True, height=300)

# ---------------------------------------------------------------------------
# TAB: Detail per Unit/Kriteria
# ---------------------------------------------------------------------------
with tab_detail:
    if tampilan == "Per Unit":
        unit_list = DATA["final_unit"].sort_values("V4_GB_MAPE")["EQUIP NAME"].tolist()
        pilihan = st.selectbox("Pilih unit", unit_list)
        row = DATA["final_unit"][DATA["final_unit"]["EQUIP NAME"] == pilihan].iloc[0]

        top_combos_u = (DATA["v2b_unit_12"][DATA["v2b_unit_12"]["EQUIP NAME"] == pilihan]
                        .sort_values("MAPE").reset_index(drop=True))
        best1_u = top_combos_u.iloc[0] if len(top_combos_u) >= 1 else None
        best2_u = top_combos_u.iloc[1] if len(top_combos_u) >= 2 else None

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Gradient Boosting (Model Final)**")
            st.write(f"Varian data-prep: `{row.get('V4_GB_VARIAN')}`")
            st.write(f"MAPE: {row.get('V4_GB_MAPE'):.2f}% | RMSE: {row.get('V4_GB_RMSE'):.2f}")
        with c2:
            st.markdown("**Kombinasi Terbaik Pertama**")
            if best1_u is not None:
                st.write(f"Model: `{best1_u['MODEL']}` | Varian: `{best1_u['VARIAN']}`")
                st.write(f"MAPE: {best1_u['MAPE']:.2f}% | RMSE: {best1_u['RMSE']:.2f}")
            else:
                st.write(f"Model: `{row.get('V2B_BEST_MODEL')}` | Varian: `{row.get('V2B_BEST_VARIAN')}`")
                st.write(f"MAPE: {row.get('V2B_BEST_MAPE'):.2f}% | RMSE: {row.get('V2B_BEST_RMSE'):.2f}")
        with c3:
            st.markdown("**Kombinasi Terbaik Kedua**")
            if best2_u is not None:
                st.write(f"Model: `{best2_u['MODEL']}` | Varian: `{best2_u['VARIAN']}`")
                st.write(f"MAPE: {best2_u['MAPE']:.2f}% | RMSE: {best2_u['RMSE']:.2f}")
            else:
                st.write("-")

        st.subheader("Plot Evaluasi Testing (periode evaluasi)")
        eval_df = eval_unit_on_test_cached(pilihan)
        if eval_df is None:
            st.warning("Tidak bisa menghasilkan plot evaluasi testing untuk unit ini (data tidak cukup).")
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=eval_df["TAHUN_BULAN"].astype(str),
                y=eval_df["ACTUAL"],
                mode="lines+markers",
                name="Actual",
                line=dict(color="#2ca02c"),
                hovertemplate="%{y:.2f} jam<extra></extra>"
            ))
            # Ambil titik aktual terakhir masa training (2025-09) agar garis prediksi testing menyambung langsung
            last_train_actual = eval_df[eval_df["SET"] == "train"].iloc[[-1]].copy()
            last_train_actual["PRED"] = last_train_actual["ACTUAL"]
            te_raw = eval_df[eval_df["SET"] == "test"]
            te = pd.concat([last_train_actual, te_raw], ignore_index=True) if not te_raw.empty else te_raw
            fig.add_trace(go.Scatter(
                x=te["TAHUN_BULAN"].astype(str),
                y=te["PRED"],
                mode="lines+markers",
                name=f"Model Final (GB + {row.get('V4_GB_VARIAN')})",
                line=dict(color="orange"),
                hovertemplate="%{y:.2f} jam<extra></extra>"
            ))
            if best1_u is not None:
                sub1_u = DATA["v2b_unit_raw"][
                    (DATA["v2b_unit_raw"]["EQUIP NAME"] == pilihan)
                    & (DATA["v2b_unit_raw"]["MODEL"] == best1_u["MODEL"])
                    & (DATA["v2b_unit_raw"]["VARIAN"] == best1_u["VARIAN"])
                ].sort_values("TAHUN_BULAN")[["TAHUN_BULAN", "PRED"]]
                if not sub1_u.empty:
                    te_b1 = pd.concat([last_train_actual[["TAHUN_BULAN", "PRED"]], sub1_u], ignore_index=True)
                    fig.add_trace(go.Scatter(
                        x=te_b1["TAHUN_BULAN"].astype(str),
                        y=te_b1["PRED"],
                        mode="lines+markers",
                        name=f"Terbaik 1 ({best1_u['MODEL']} + {best1_u['VARIAN']})",
                        line=dict(color="#00b4d8", dash="dash"),
                        hovertemplate="%{y:.2f} jam<extra></extra>"
                    ))
            if best2_u is not None:
                sub2_u = DATA["v2b_unit_raw"][
                    (DATA["v2b_unit_raw"]["EQUIP NAME"] == pilihan)
                    & (DATA["v2b_unit_raw"]["MODEL"] == best2_u["MODEL"])
                    & (DATA["v2b_unit_raw"]["VARIAN"] == best2_u["VARIAN"])
                ].sort_values("TAHUN_BULAN")[["TAHUN_BULAN", "PRED"]]
                if not sub2_u.empty:
                    te_b2 = pd.concat([last_train_actual[["TAHUN_BULAN", "PRED"]], sub2_u], ignore_index=True)
                    fig.add_trace(go.Scatter(
                        x=te_b2["TAHUN_BULAN"].astype(str),
                        y=te_b2["PRED"],
                        mode="lines+markers",
                        name=f"Terbaik 2 ({best2_u['MODEL']} + {best2_u['VARIAN']})",
                        line=dict(color="#c77dff", dash="dot"),
                        hovertemplate="%{y:.2f} jam<extra></extra>"
                    ))
            fig.update_layout(
                xaxis_title="Bulan",
                yaxis_title="Operating Hours (jam)",
                yaxis=dict(rangemode="tozero"),
                hovermode="x unified",
                height=440
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"Plot Actual s/d Future Forecast ({horizon} bulan ke depan)")
        hist = DATA["monthly_full"][DATA["monthly_full"]["EQUIP NAME"] == pilihan].sort_values("TAHUN_BULAN")
        fut_raw = DATA["future_forecast"][
            (DATA["future_forecast"]["EQUIP NAME"] == pilihan)
            & (DATA["future_forecast"]["HORIZON_BULAN_KE"] <= horizon)
        ].sort_values("TAHUN_BULAN")
        if not hist.empty and not fut_raw.empty:
            last_hist = pd.DataFrame({
                "TAHUN_BULAN": [hist["TAHUN_BULAN"].iloc[-1]],
                "FORECAST_OPERATING_HOURS": [hist.get("OPERATING_HOURS", hist.get("UTILITAS")).iloc[-1]],
                "FORECAST_UTILITAS": [hist.get("OPERATING_HOURS", hist.get("UTILITAS")).iloc[-1]],
            })
            fut = pd.concat([last_hist, fut_raw], ignore_index=True)
        else:
            fut = fut_raw
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=hist["TAHUN_BULAN"].astype(str),
            y=hist.get("OPERATING_HOURS", hist.get("UTILITAS")),
            mode="lines+markers",
            name="Actual (historis)",
            line=dict(color="#1f77b4"),
            hovertemplate="%{y:.2f} jam<extra></extra>"
        ))
        fig2.add_trace(go.Scatter(
            x=fut["TAHUN_BULAN"].astype(str),
            y=fut.get("FORECAST_OPERATING_HOURS", fut.get("FORECAST_UTILITAS")),
            mode="lines+markers",
            name="Future Forecast",
            line=dict(color="crimson", dash="dash"),
            hovertemplate="%{y:.2f} jam<extra></extra>"
        ))
        fig2.update_layout(
            xaxis_title="Bulan",
            yaxis_title="Operating Hours (jam)",
            yaxis=dict(rangemode="tozero"),
            hovermode="x unified",
            height=420
        )
        st.plotly_chart(fig2, use_container_width=True)
        if horizon > 3:
            st.caption(
                "Catatan: forecast di luar 3 bulan pertama dihasilkan scr rolling/recursive "
                "(lag memakai hasil prediksi sendiri), sehingga potensi error lebih besar "
                "dibanding 3 bulan pertama."
            )

    else:  # Per Kriteria
        krit_list = DATA["final_krit"].sort_values("V4_GB_MAPE")["KRITERIA_ID"].tolist()
        pilihan_k = st.selectbox("Pilih kriteria", krit_list)
        krow = DATA["final_krit"][DATA["final_krit"]["KRITERIA_ID"] == pilihan_k].iloc[0]

        top_combos_k = (DATA["v2b_krit_12"][DATA["v2b_krit_12"]["KRITERIA_ID"] == pilihan_k]
                        .sort_values("MAPE").reset_index(drop=True))
        best1_k = top_combos_k.iloc[0] if len(top_combos_k) >= 1 else None
        best2_k = top_combos_k.iloc[1] if len(top_combos_k) >= 2 else None

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Gradient Boosting (Model Final)**")
            st.write(f"Varian data-prep: `{krow.get('V4_GB_VARIAN')}`")
            st.write(f"MAPE: {krow.get('V4_GB_MAPE'):.2f}% | RMSE: {krow.get('V4_GB_RMSE'):.2f}")
        with c2:
            st.markdown("**Kombinasi Terbaik Pertama**")
            if best1_k is not None:
                st.write(f"Model: `{best1_k['MODEL']}` | Varian: `{best1_k['VARIAN']}`")
                st.write(f"MAPE: {best1_k['MAPE']:.2f}% | RMSE: {best1_k['RMSE']:.2f}")
            else:
                st.write(f"Model: `{krow.get('V2B_BEST_MODEL')}` | Varian: `{krow.get('V2B_BEST_VARIAN')}`")
                st.write(f"MAPE: {krow.get('V2B_BEST_MAPE'):.2f}% | RMSE: {krow.get('V2B_BEST_RMSE'):.2f}")
        with c3:
            st.markdown("**Kombinasi Terbaik Kedua**")
            if best2_k is not None:
                st.write(f"Model: `{best2_k['MODEL']}` | Varian: `{best2_k['VARIAN']}`")
                st.write(f"MAPE: {best2_k['MAPE']:.2f}% | RMSE: {best2_k['RMSE']:.2f}")
            else:
                st.write("-")

        n_anggota = DATA["kriteria"][DATA["kriteria"]["KRITERIA_ID"] == pilihan_k]["EQUIP NAME"].nunique()
        st.caption(f"Jumlah unit anggota: {n_anggota}")

        st.subheader("Plot Evaluasi Testing Kriteria (periode evaluasi)")
        eval_df_k = eval_kriteria_on_test_cached(pilihan_k)
        if eval_df_k is None:
            st.warning("Tidak bisa menghasilkan plot evaluasi testing untuk kriteria ini (data tidak cukup).")
        else:
            fig_eval_k = go.Figure()
            fig_eval_k.add_trace(go.Scatter(
                x=eval_df_k["TAHUN_BULAN"].astype(str),
                y=eval_df_k["ACTUAL"],
                mode="lines+markers",
                name="Actual (total kriteria)",
                line=dict(color="#2ca02c"),
                hovertemplate="%{y:.2f} jam<extra></extra>"
            ))
            # Ambil titik aktual terakhir masa training (2025-09) agar garis prediksi testing menyambung langsung
            last_train_k = eval_df_k[eval_df_k["SET"] == "train"].iloc[[-1]].copy()
            last_train_k["PRED"] = last_train_k["ACTUAL"]
            te_raw_k = eval_df_k[eval_df_k["SET"] == "test"]
            te_k = pd.concat([last_train_k, te_raw_k], ignore_index=True) if not te_raw_k.empty else te_raw_k
            fig_eval_k.add_trace(go.Scatter(
                x=te_k["TAHUN_BULAN"].astype(str),
                y=te_k["PRED"],
                mode="lines+markers",
                name=f"Model Final (GB + {krow.get('V4_GB_VARIAN')})",
                line=dict(color="orange"),
                hovertemplate="%{y:.2f} jam<extra></extra>"
            ))
            if best1_k is not None:
                sub1_k = (DATA["v2b_krit_raw"][
                    (DATA["v2b_krit_raw"]["KRITERIA_ID"] == pilihan_k)
                    & (DATA["v2b_krit_raw"]["MODEL"] == best1_k["MODEL"])
                    & (DATA["v2b_krit_raw"]["VARIAN"] == best1_k["VARIAN"])
                ].groupby("TAHUN_BULAN")[["PRED"]].sum().reset_index().sort_values("TAHUN_BULAN"))
                if not sub1_k.empty:
                    te_kb1 = pd.concat([last_train_k[["TAHUN_BULAN", "PRED"]], sub1_k], ignore_index=True)
                    fig_eval_k.add_trace(go.Scatter(
                        x=te_kb1["TAHUN_BULAN"].astype(str),
                        y=te_kb1["PRED"],
                        mode="lines+markers",
                        name=f"Terbaik 1 ({best1_k['MODEL']} + {best1_k['VARIAN']})",
                        line=dict(color="#00b4d8", dash="dash"),
                        hovertemplate="%{y:.2f} jam<extra></extra>"
                    ))
            if best2_k is not None:
                sub2_k = (DATA["v2b_krit_raw"][
                    (DATA["v2b_krit_raw"]["KRITERIA_ID"] == pilihan_k)
                    & (DATA["v2b_krit_raw"]["MODEL"] == best2_k["MODEL"])
                    & (DATA["v2b_krit_raw"]["VARIAN"] == best2_k["VARIAN"])
                ].groupby("TAHUN_BULAN")[["PRED"]].sum().reset_index().sort_values("TAHUN_BULAN"))
                if not sub2_k.empty:
                    te_kb2 = pd.concat([last_train_k[["TAHUN_BULAN", "PRED"]], sub2_k], ignore_index=True)
                    fig_eval_k.add_trace(go.Scatter(
                        x=te_kb2["TAHUN_BULAN"].astype(str),
                        y=te_kb2["PRED"],
                        mode="lines+markers",
                        name=f"Terbaik 2 ({best2_k['MODEL']} + {best2_k['VARIAN']})",
                        line=dict(color="#c77dff", dash="dot"),
                        hovertemplate="%{y:.2f} jam<extra></extra>"
                    ))
            fig_eval_k.update_layout(
                xaxis_title="Bulan",
                yaxis_title="Total Operating Hours (jam)",
                yaxis=dict(rangemode="tozero"),
                hovermode="x unified",
                height=440
            )
            st.plotly_chart(fig_eval_k, use_container_width=True)

        st.subheader(f"Plot Actual s/d Future Forecast Kriteria ({horizon} bulan ke depan)")
        st.caption(
            "Forecast level kriteria = total forecast seluruh unit anggota kriteria ini, dihasilkan "
            "dari satu model yang dilatih memakai data gabungan seluruh unit anggota."
        )
        with st.spinner("Melatih ulang model & menghasilkan forecast kriteria..."):
            total_fc, per_unit_fc = retrain_forecast_kriteria_cached(pilihan_k, horizon)

        val_col_mf = "OPERATING_HOURS" if "OPERATING_HOURS" in DATA["monthly_full"].columns else "UTILITAS"
        hist_k = (DATA["monthly_full"].merge(DATA["kriteria"][["EQUIP NAME", "KRITERIA_ID"]], on="EQUIP NAME")
                  .query("KRITERIA_ID == @pilihan_k")
                  .groupby("TAHUN_BULAN")[val_col_mf].sum().reset_index().sort_values("TAHUN_BULAN"))
        if "OPERATING_HOURS" not in hist_k.columns and "UTILITAS" in hist_k.columns:
            hist_k["OPERATING_HOURS"] = hist_k["UTILITAS"]
        elif "UTILITAS" not in hist_k.columns and "OPERATING_HOURS" in hist_k.columns:
            hist_k["UTILITAS"] = hist_k["OPERATING_HOURS"]

        if total_fc is None:
            st.warning("Tidak bisa menghasilkan forecast untuk kriteria ini (data tidak cukup).")
        else:
            if not hist_k.empty and not total_fc.empty:
                last_hist_k = pd.DataFrame({
                    "TAHUN_BULAN": [hist_k["TAHUN_BULAN"].iloc[-1]],
                    "FORECAST_OPERATING_HOURS": [hist_k.get("OPERATING_HOURS", hist_k.get("UTILITAS")).iloc[-1]],
                    "FORECAST_UTILITAS": [hist_k.get("OPERATING_HOURS", hist_k.get("UTILITAS")).iloc[-1]],
                })
                total_fc_conn = pd.concat([last_hist_k, total_fc], ignore_index=True)
            else:
                total_fc_conn = total_fc
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=hist_k["TAHUN_BULAN"].astype(str),
                y=hist_k.get("OPERATING_HOURS", hist_k.get("UTILITAS")),
                mode="lines+markers",
                name="Actual (historis, total kriteria)",
                line=dict(color="#1f77b4"),
                hovertemplate="%{y:.2f} jam<extra></extra>"
            ))
            fig3.add_trace(go.Scatter(
                x=total_fc_conn["TAHUN_BULAN"].astype(str),
                y=total_fc_conn.get("FORECAST_OPERATING_HOURS", total_fc_conn.get("FORECAST_UTILITAS")),
                mode="lines+markers",
                name="Future Forecast (total kriteria)",
                line=dict(color="crimson", dash="dash"),
                hovertemplate="%{y:.2f} jam<extra></extra>"
            ))
            fig3.update_layout(
                xaxis_title="Bulan",
                yaxis_title="Total Operating Hours (jam)",
                yaxis=dict(rangemode="tozero"),
                hovermode="x unified",
                height=420
            )
            st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB: Rolling vs Direct
# ---------------------------------------------------------------------------
with tab_rolling:
    st.subheader("Perbandingan Metode Forecasting: Rolling vs Direct")
    df_roll = DATA["rolling_unit"] if tampilan == "Per Unit" else DATA["rolling_krit"]
    roll_rename = {
        "EQUIP NAME": "Nama Unit",
        "KRITERIA_ID": "Kriteria ID",
        "VARIAN": "Varian Data-Prep",
        "MAPE_DIRECT": "MAPE Direct (%)",
        "RMSE_DIRECT": "RMSE Direct",
        "MAPE_ROLLING": "MAPE Rolling (%)",
        "RMSE_ROLLING": "RMSE Rolling",
        "IDENTIK": "Identik",
        "LEBIH_RENDAH": "Metode Lebih Baik",
    }
    st.dataframe(df_roll.rename(columns=roll_rename), use_container_width=True, height=450)
    st.caption(
        "Forecasting rolling menghasilkan nilai prediksi secara rekursif di mana input lag menggunakan output prediksi periode sebelumnya. "
        "Direct forecasting menghasilkan evaluasi lebih stabil, namun untuk proyeksi masa depan di luar data historis, "
        "pendekatan rolling adalah metode yang digunakan."
    )
