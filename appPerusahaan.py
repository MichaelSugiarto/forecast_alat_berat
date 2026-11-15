# -*- coding: utf-8 -*-
"""
appPerusahaan.py: Dashboard Prediksi Operating Hours Alat Berat
=========================================================
Tampilan sederhana: upload data -> pilih unit -> lihat plot actual s/d forecast.
Tidak menampilkan metrik error (MAPE/RMSE) ke pengguna, metrik error disimpan khusus untuk appDemo.py.

Alur:
1. Pengguna upload file Excel mentah terbaru (BBM AAB per tahun, cost&bbm HP&Type, Container
   per tahun, Curah Hujan).
2. pipeline_lib.build_monthly_full() menjalankan ETL dari file-file itu.
3. Setiap unit di-fit ULANG (bukan dicari kombinasi baru) memakai konfigurasi data-prep &
   hyperparameter GB final yang SUDAH ditentukan sebelumnya (dari ./checkpoints_v4/h3bulan).
   Unit yang diexclude terdaftar pada tab "Unit Diexclude".
4. Forecast ke depan (rolling), default 3 bulan, bisa ditarik sampai 12 bulan.

Jalankan: streamlit run appPerusahaan.py
"""

import importlib
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import pipeline_lib as pl
importlib.reload(pl)

st.set_page_config(page_title="Prediksi Operating Hours Alat Berat", layout="wide")

BASE_DIR = Path("./checkpoints_v4")
H3_DIR = (BASE_DIR / "rev_h3") if (BASE_DIR / "rev_h3").exists() else (BASE_DIR / "h3bulan")

st.title("Prediksi Operating Hours Alat Berat")
st.caption("Sistem Prediksi Operating Hours Armada Alat Berat")

if "hasil" not in st.session_state:
    st.session_state["hasil"] = None

# ---------------------------------------------------------------------------
# Bagian upload data
# ---------------------------------------------------------------------------
st.header("1. Upload Data")

col_kiri, col_kanan = st.columns(2)
with col_kiri:
    st.subheader("Data BBM AAB (boleh lebih dari 1 file, per tahun)")
    bbm_uploads = st.file_uploader("Drag and drop files here", type=["xlsx"],
                                    accept_multiple_files=True, key="bbm")
    st.subheader("Detail Alat Berat (cost & bbm HP & Type, 1 file)")
    cost_upload = st.file_uploader("Drag and drop file here", type=["xlsx"], key="cost")

with col_kanan:
    st.subheader("Data Container (boleh lebih dari 1 file, per tahun)")
    container_uploads = st.file_uploader("Drag and drop files here", type=["xlsx"],
                                          accept_multiple_files=True, key="container")
    st.subheader("Data Curah Hujan (1 file)")
    rainfall_upload = st.file_uploader("Drag and drop file here", type=["xlsx"], key="rain")

st.caption(
    "Nama file BBM AAB & Container tidak harus mengandung tahun, tahun diambil otomatis "
    "dari isi atau urutan file yang diupload."
)

def _infer_year_from_name(name, fallback_years):
    import re
    m = re.search(r"(20\d{2})", name)
    if m:
        return int(m.group(1))
    return fallback_years.pop(0)

jalankan = st.button("Jalankan Proses Forecast", type="primary")

if jalankan:
    if not (bbm_uploads and cost_upload and container_uploads and rainfall_upload):
        st.error("Semua jenis data (BBM AAB, Detail Alat Berat, Container, Curah Hujan) wajib diupload.")
        st.stop()

    with st.spinner("Memproses data (ETL)..."):
        tmp_dir = Path("./_uploaded_tmp")
        tmp_dir.mkdir(exist_ok=True)

        guess_years = [2023, 2024, 2025, 2026, 2027]
        bbm_files = {}
        for f in bbm_uploads:
            yr = _infer_year_from_name(f.name, guess_years)
            p = tmp_dir / f"BBM_{yr}.xlsx"
            p.write_bytes(f.getbuffer())
            bbm_files[yr] = p

        guess_years2 = [2023, 2024, 2025, 2026, 2027]
        container_files = {}
        for f in container_uploads:
            yr = _infer_year_from_name(f.name, guess_years2)
            p = tmp_dir / f"Container_{yr}.xlsx"
            p.write_bytes(f.getbuffer())
            container_files[yr] = p

        cost_path = tmp_dir / "cost_bbm.xlsx"
        cost_path.write_bytes(cost_upload.getbuffer())
        rain_path = tmp_dir / "rainfall.xlsx"
        rain_path.write_bytes(rainfall_upload.getbuffer())

        try:
            etl_result = pl.build_monthly_full(bbm_files, container_files, cost_path, rain_path)
        except Exception as e:
            st.error(f"Gagal memproses data: {e}")
            st.stop()

    monthly_full = etl_result["monthly_full"]
    kriteria = etl_result["kriteria"]

    # Pastikan nama unit di monthly_full sinkron dengan format konfigurasi model
    ref_candidates = [
        Path("./checkpoints_v4/rev_h3/mapping_unit_dan_kriteria.xlsx"),
        Path("./checkpoints_v4/mapping_unit_dan_kriteria.xlsx"),
    ]
    ref_path = next((p for p in ref_candidates if p.exists()), None)
    if ref_path is not None:
        try:
            df_ref = pd.read_excel(ref_path, sheet_name="Mapping_Unit")
            old_to_k_unit = dict(zip(df_ref["EQUIP_NAME_LAMA"], df_ref["EQUIP_NAME_BARU"]))
            if monthly_full["EQUIP NAME"].astype(str).str.startswith("UNIT_").any():
                monthly_full["EQUIP NAME"] = monthly_full["EQUIP NAME"].map(lambda u: old_to_k_unit.get(u, u))
            if kriteria["EQUIP NAME"].astype(str).str.startswith("UNIT_").any():
                kriteria["EQUIP NAME"] = kriteria["EQUIP NAME"].map(lambda u: old_to_k_unit.get(u, u))
        except Exception:
            pass

    with st.spinner("Menyiapkan forecast per unit..."):
        final_unit_cfg = pl.load_final_config(H3_DIR, level="unit")
        exog_future = pl.estimate_future_exog(monthly_full, horizon=12)

        forecast_frames = []
        gagal_retrain = []
        tidak_ada_config = []

        units_in_data = set(monthly_full["EQUIP NAME"].unique())
        units_with_cfg = set(final_unit_cfg["EQUIP NAME"].unique())

        for u in sorted(units_in_data - units_with_cfg):
            if u in pl.EXCLUDED_NON_OPERATIONAL_UNITS or u in pl.EXCLUDED_NON_OPERATIONAL_NAMES:
                continue
            tidak_ada_config.append(u)

        for _, row in final_unit_cfg.iterrows():
            if row["EQUIP NAME"] not in units_in_data:
                continue
            out = pl.retrain_and_forecast_unit(monthly_full, row, exog_future, horizon=12)
            if out is None:
                gagal_retrain.append(row["EQUIP NAME"])
            else:
                forecast_frames.append(out)

        future_forecast_df = (pd.concat(forecast_frames, ignore_index=True)
                               if forecast_frames else pd.DataFrame(
            columns=["EQUIP NAME", "TAHUN_BULAN", "HORIZON_BULAN_KE", "FORECAST_OPERATING_HOURS", "FORECAST_UTILITAS", "VARIAN"]))

        # Rangkuman unit yang diexclude berdasarkan kriteria kelayakan
        excluded_df = pl.load_excluded_summary(H3_DIR)

        # Catat unit baru di data upload yang belum memiliki konfigurasi model atau gagal retrain
        extra_exc_rows = []
        known_exc_units = set(excluded_df["EQUIP NAME"]) if not excluded_df.empty else set()
        for u in tidak_ada_config:
            if u not in known_exc_units:
                extra_exc_rows.append({
                    "EQUIP NAME": u,
                    "ALASAN": "Unit baru, belum memiliki konfigurasi model terlatih"
                })
        for u in gagal_retrain:
            if u not in known_exc_units:
                extra_exc_rows.append({
                    "EQUIP NAME": u,
                    "ALASAN": "Data historis tidak mencukupi untuk proses retraining (kurang dari 6 bulan)"
                })
        if extra_exc_rows:
            excluded_df = pd.concat([excluded_df, pd.DataFrame(extra_exc_rows)], ignore_index=True)

    st.session_state["hasil"] = {
        "monthly_full": monthly_full,
        "kriteria": kriteria,
        "future_forecast": future_forecast_df,
        "excluded": excluded_df,
    }
    st.success(
        f"Selesai. {future_forecast_df['EQUIP NAME'].nunique()} unit berhasil diproyeksikan, "
        f"{len(excluded_df)} unit diexclude."
    )

# ---------------------------------------------------------------------------
# Bagian hasil
# ---------------------------------------------------------------------------
if st.session_state["hasil"] is not None:
    hasil = st.session_state["hasil"]
    monthly_full = hasil["monthly_full"]
    future_forecast_df = hasil["future_forecast"]
    excluded_df = hasil["excluded"]

    st.header("2. Hasil Prediksi")
    tab_forecast, tab_exclude = st.tabs(["Prediksi per Unit", "Unit Diexclude"])

    # Siapkan tabel Unit Diexclude terlebih dahulu agar ikut masuk ke file Excel export (Sheet 2)
    df_exc = excluded_df.copy()
    reason_map = {
        "nol total di salah satu tahun train": "Data operating hours pada salah satu tahun periode data train bernilai nol semua",
        "Nol total di salah satu tahun train": "Data operating hours pada salah satu tahun periode data train bernilai nol semua",
        "test bernilai nol seluruhnya": "Data operating hours pada periode data test bernilai nol semua",
        "Test bernilai nol seluruhnya": "Data operating hours pada periode data test bernilai nol semua",
    }
    if "TAHAP" in df_exc.columns:
        df_exc = df_exc[~df_exc["TAHAP"].astype(str).str.contains("data baru", case=False, na=False)]
    if "ALASAN" in df_exc.columns:
        df_exc = df_exc[~df_exc["ALASAN"].astype(str).str.contains("review MAPE|data baru|threshold|toleransi", case=False, na=False)]
        df_exc["ALASAN"] = (
            df_exc["ALASAN"].astype(str).str.strip()
            .map(lambda s: reason_map.get(s, s[0].upper() + s[1:] if len(s) > 0 else s))
            .str.replace("utilitas", "operating hours", case=False)
        )
    excluded_display = (
        df_exc[["EQUIP NAME", "ALASAN"]]
        .sort_values("EQUIP NAME")
        .reset_index(drop=True)
        .rename(columns={
            "EQUIP NAME": "Nama Unit",
            "ALASAN": "Alasan",
        })
    )

    with tab_forecast:
        unit_list = sorted(future_forecast_df["EQUIP NAME"].unique())
        if not unit_list:
            st.warning("Tidak ada unit dengan hasil forecast.")
        else:
            pilihan_units = st.multiselect(
                "Pilih unit (bisa lebih dari satu)",
                unit_list,
                default=[unit_list[0]] if unit_list else []
            )
            horizon = st.slider("Tampilkan forecast berapa bulan ke depan", min_value=3, max_value=12, value=3)
            if horizon > 3:
                st.info(
                    "Forecast di atas 3 bulan memiliki tingkat akurasi yang lebih rendah dibanding 3 bulan pertama."
                )

            if not pilihan_units:
                st.info("Silakan pilih minimal satu unit untuk menampilkan grafik prediksi.")
            else:
                unit_colors = [
                    "#1f77b4", "#ff7f0e", "#2ca02c", "#00b4d8", "#c77dff",
                    "#ffd166", "#f72585", "#4cc9f0", "#80ed99", "#fb8500",
                ]
                fig = go.Figure()
                multi_mode = len(pilihan_units) > 1
                for idx, u in enumerate(pilihan_units):
                    hist = monthly_full[monthly_full["EQUIP NAME"] == u].sort_values("TAHUN_BULAN")
                    fut_raw = future_forecast_df[
                        (future_forecast_df["EQUIP NAME"] == u)
                        & (future_forecast_df["HORIZON_BULAN_KE"] <= horizon)
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

                    col_actual = unit_colors[idx % len(unit_colors)] if multi_mode else "#1f77b4"
                    col_forecast = unit_colors[idx % len(unit_colors)] if multi_mode else "crimson"

                    fig.add_trace(go.Scatter(
                        x=hist["TAHUN_BULAN"].astype(str),
                        y=hist.get("OPERATING_HOURS", hist.get("UTILITAS")),
                        mode="lines+markers",
                        name=f"Actual ({u})" if multi_mode else "Actual",
                        legendgroup=u,
                        line=dict(color=col_actual),
                        hovertemplate="%{y:.2f} jam<extra></extra>"
                    ))
                    fig.add_trace(go.Scatter(
                        x=fut["TAHUN_BULAN"].astype(str),
                        y=fut.get("FORECAST_OPERATING_HOURS", fut.get("FORECAST_UTILITAS")),
                        mode="lines+markers",
                        name=f"Forecast ({u})" if multi_mode else "Forecast",
                        legendgroup=u,
                        line=dict(color=col_forecast, dash="dash"),
                        hovertemplate="%{y:.2f} jam<extra></extra>"
                    ))
                fig.update_layout(
                    xaxis_title="Bulan",
                    yaxis_title="Operating Hours (jam)",
                    yaxis=dict(rangemode="tozero"),
                    hovermode="x unified",
                    height=480 if multi_mode else 450
                )
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("Export")
            export_df = (
                future_forecast_df[future_forecast_df["HORIZON_BULAN_KE"] <= horizon][
                    ["EQUIP NAME", "TAHUN_BULAN", "FORECAST_OPERATING_HOURS" if "FORECAST_OPERATING_HOURS" in future_forecast_df.columns else "FORECAST_UTILITAS"]
                ]
                .sort_values(["EQUIP NAME", "TAHUN_BULAN"])
                .reset_index(drop=True)
                .rename(columns={"EQUIP NAME": "UNIT", "TAHUN_BULAN": "BULAN", "FORECAST_OPERATING_HOURS": "FORECAST", "FORECAST_UTILITAS": "FORECAST"})
            )
            export_path = Path("./_uploaded_tmp/hasil_forecast_export.xlsx")
            export_path.parent.mkdir(parents=True, exist_ok=True)
            with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
                export_df.to_excel(writer, sheet_name="Hasil_Forecast", index=False)
                excluded_display.to_excel(writer, sheet_name="Unit_Diexclude", index=False)
            with open(export_path, "rb") as f:
                st.download_button("Download Excel Hasil Forecast & Unit yang Diexclude", f,
                                    file_name="hasil_forecast_operating_hours.xlsx")

    with tab_exclude:
        st.caption("Daftar unit yang diexclude dari sistem prediksi beserta alasannya.")
        st.dataframe(excluded_display, use_container_width=True, height=450)
else:
    st.info("Upload data di atas, lalu klik \"Jalankan Proses Forecast\" untuk melihat hasil.")