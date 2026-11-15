# analisis_pacf_spearman.py
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import pacf
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Path relatif dinamis
BASE_DIR = Path(__file__).resolve().parent if '__file__' in globals() else Path('.')
sys.path.insert(0, str(BASE_DIR))
import pipeline_lib as pl

# 1. Load dataset monthly_full
monthly_full = pl.load_monthly_full_checkpoint(Path("./checkpoints_v4"))

# Muat mapping kriteria agar nama unit selaras dengan eda_14 (UNIT_0001) maupun K##_UNIT_###
map_path = Path("./checkpoints_v4/rev_h3/mapping_unit_dan_kriteria.xlsx")
if not map_path.exists():
    map_path = Path("./checkpoints_v4/mapping_unit_dan_kriteria.xlsx")
if not map_path.exists():
    map_path = BASE_DIR / "mapping_unit_dan_kriteria.xlsx"

lama_to_baru = {}
baru_to_lama = {}
if map_path.exists():
    try:
        df_m = pd.read_excel(map_path)
        lama_to_baru = dict(zip(df_m["EQUIP_NAME_LAMA"], df_m["EQUIP_NAME_BARU"]))
        baru_to_lama = dict(zip(df_m["EQUIP_NAME_BARU"], df_m["EQUIP_NAME_LAMA"]))
    except Exception as e:
        print(f"Peringatan membaca mapping: {e}")

units = sorted(monthly_full['EQUIP NAME'].unique())
results = []
pacf_cutoffs = []

col_target = 'OPERATING_HOURS' if 'OPERATING_HOURS' in monthly_full.columns else 'UTILITAS'

for u in units:
    sub = monthly_full[monthly_full['EQUIP NAME'] == u].sort_values('TAHUN_BULAN')
    if len(sub) < 12:
        continue
    y = sub[col_target].values
    vc = sub['VOLUME_CONTAINER'].values
    
    if np.std(y) > 0 and np.std(vc) > 0:
        r_p, _ = stats.pearsonr(y, vc)
        r_s, _ = stats.spearmanr(y, vc)
        is_spearman = abs(r_s) > abs(r_p)
        
        sig_thresh = 1.96 / np.sqrt(len(y))
        try:
            p_vals = pacf(y, nlags=min(6, len(y)//2 - 1))
            sig_lags = [i for i, val in enumerate(p_vals[1:], 1) if abs(val) > sig_thresh]
            max_sig = max(sig_lags) if sig_lags else 0
            pacf_cutoffs.append(max_sig)
        except Exception:
            max_sig = np.nan

        # Format nama unit lama (misal UNIT_0004) dan kriteria baru (misal K01_UNIT_004)
        nama_lama = baru_to_lama.get(u, u)
        nama_baru = lama_to_baru.get(u, u)

        results.append({
            'EQUIP NAME': nama_baru,
            'KODE_KRITERIA': nama_baru.split('_')[0] if '_' in nama_baru else '',
            'PEARSON_VC': r_p,
            'SPEARMAN_VC': r_s,
            'SPEARMAN_STRONGER': is_spearman,
            'MAX_SIG_PACF_LAG': max_sig
        })

df_res = pd.DataFrame(results)
spearman_wins = df_res['SPEARMAN_STRONGER'].sum()
pearson_wins = len(df_res) - spearman_wins
total_units = len(df_res)

print(f"Total Unit Dievaluasi: {total_units}")
print(f"Spearman Lebih Kuat: {spearman_wins} unit ({spearman_wins/total_units*100:.2f}%)")
print(f"Pearson Lebih Kuat: {pearson_wins} unit ({pearson_wins/total_units*100:.2f}%)")
print("Distribusi Lag Maksimum PACF Signifikan:")
lag_dist = pd.Series(pacf_cutoffs).value_counts().sort_index()
print(lag_dist)

out_csv = BASE_DIR / "analisis_pacf_spearman.csv"
df_res.to_csv(out_csv, index=False)
out_csv_rev = BASE_DIR / "checkpoints_v4" / "rev_h3" / "analisis_pacf_spearman.csv"
if out_csv_rev.parent.exists():
    df_res.to_csv(out_csv_rev, index=False)
print(f"Hasil detail tersimpan di: {out_csv} dan {out_csv_rev}")

# 2. Visualisasi Publikasi (Diagram Batang PACF + Diagram Lingkaran Spearman)
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Subplot 1: Distribusi Lag PACF
lags = [0, 1, 2, 3, 4, 5, 6]
counts = [lag_dist.get(i, 0) for i in lags]
bars = axes[0].bar([f"Lag {i}" for i in lags], counts, color='#1f77b4', edgecolor='black', alpha=0.85)
axes[0].set_title("Distribusi Lag Maksimum PACF Signifikan per Unit\n(Threshold = 1.96 / sqrt(N))", fontsize=12, fontweight='bold', pad=12)
axes[0].set_xlabel("Lag Signifikan Terakhir", fontsize=11, labelpad=8)
axes[0].set_ylabel("Jumlah Unit", fontsize=11, labelpad=8)
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    pct = (yval / total_units) * 100
    axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{int(yval)}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=9)
axes[0].set_ylim(0, max(counts) * 1.2)

# Subplot 2: Proporsi Spearman vs Pearson
labels = [
    f"Spearman Lebih Kuat ({spearman_wins} unit, {spearman_wins/total_units*100:.1f}%)",
    f"Pearson Lebih Kuat ({pearson_wins} unit, {pearson_wins/total_units*100:.1f}%)"
]
sizes = [spearman_wins, pearson_wins]
colors = ['#2ca02c', '#ff7f0e']

wedges, texts, autotexts = axes[1].pie(
    sizes, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors,
    pctdistance=0.6,
    wedgeprops=dict(edgecolor='black', linewidth=1.2, antialiased=True)
)
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight('bold')
    at.set_color('white')

axes[1].legend(
    wedges, labels, 
    title="Hubungan Eksogen (Volume Container)", 
    loc="lower center", 
    bbox_to_anchor=(0.5, -0.22), 
    frameon=True, 
    fontsize=10
)
axes[1].set_title(f"Proporsi Dominasi Korelasi Non-Linier Monotonik\n(Spearman vs Pearson pada {total_units} Unit)", fontsize=12, fontweight='bold', pad=12)

plt.tight_layout()
out_png = BASE_DIR / "analisis_pacf_dan_spearman.png"
plt.savefig(out_png, dpi=300, bbox_inches='tight')
out_png_rev = BASE_DIR / "checkpoints_v4" / "rev_h3" / "analisis_pacf_dan_spearman.png"
if out_png_rev.parent.exists():
    plt.savefig(out_png_rev, dpi=300, bbox_inches='tight')
plt.close()
print(f"Gambar visualisasi tersimpan di: {out_png}")
