
import streamlit as st
import pandas as pd
from io import StringIO
from datetime import date

st.set_page_config(page_title="CMC Milestone Planner", page_icon="🧪", layout="wide")
st.title("🧪 CMC Milestone Planner")
st.write("Generate a phase-appropriate checklist of CMC deliverables by modality. Use this prototype to align teams quickly and export a working checklist.")

MODALITIES = ["Cell Therapy (Autologous TCR/CAR)", "Gene Therapy (AAV/LVV)", "Monoclonal Antibody (mAb)"]
STAGES = ["Pre-IND / IND-enabling", "Phase 1", "Phase 2/3 (Pivotal)", "BLA / MAA"]

TEMPLATES = {
    "Cell Therapy (Autologous TCR/CAR)": [
        {"category":"Drug Substance","item":"Process description & flow diagram (DS)","detail":"Upstream leukapheresis, activation, gene modification, expansion; visual flow with key inputs/outputs.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Substance","item":"Process control strategy (DS)","detail":"Link QTPP→CQAs→CPPs/IPC; controls for activation, transduction/editing, expansion, harvest.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Substance","item":"Raw materials strategy & risk assessments","detail":"Traceability, animal-origin assessment, supplier qualification, CoA review/acceptance.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Product","item":"DP process description & cryopreservation parameters","detail":"Formulation, fill/finish, cryoprotectant, freezing profile, storage, thaw/use instructions.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Product","item":"Container/closure & shipping validation (phase-appropriate)","detail":"Compatibility, integrity, LN2/vapor shipping qualification; chain of custody/identity.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"recommended","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Release testing panel (identity, potency, purity, safety)","detail":"Flow identity, potency (activation/cytotoxicity), viability, purity, VCN (if applicable), sterility, mycoplasma, endotoxin.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Method lifecycle (qualification/validation plan)","detail":"Define phase-appropriate method expectations; reference standards/controls strategy.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Stability program (real-time/accelerated)","detail":"Define storage, study design, timepoints; phase-appropriate acceptance criteria.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Manufacturing & Quality Systems","item":"Tech transfer package & GMP batch records","detail":"Process description, BOM, critical parameters; MBRs with phase-appropriate controls.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Manufacturing & Quality Systems","item":"Deviation/CAPA & change control processes","detail":"Phase-appropriate QMS for investigations, CAPA, and controlled changes.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Manufacturing & Quality Systems","item":"COI/COC & logistics plan","detail":"Chain of identity and custody controls; scheduling, shipping, receiving, thaw/use.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Regulatory (Module 3)","item":"3.2.S (DS) sections draft","detail":"Controls of materials, manufacturing process, controls of critical steps & intermediates.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Regulatory (Module 3)","item":"3.2.P (DP) sections draft","detail":"Formulation, container/closure, manufacturing process, control of excipients/drug product.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
    ],
    "Gene Therapy (AAV/LVV)": [
        {"category":"Drug Substance","item":"Vector process description & flow diagram","detail":"Upstream production (AAV or LVV), harvest, clarification, chromatography/UFDF, bulk DS.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Substance","item":"Process control strategy (vector DS)","detail":"CPPs/IPC for production and purification; raw material risk strategy.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Product","item":"DP process description & formulation","detail":"Buffer/excipient selection, fill/finish parameters, container/closure compatibility.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Vector release panel","detail":"Titer, potency, purity (empty/full for AAV), HCP/HCDNA, Benzonase, sterility, mycoplasma, endotoxin, residuals.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Replication-competent virus testing (RCL/RCA)","detail":"Phase-appropriate plan for LVV (RCL) or AAV (RCA) where applicable.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Manufacturing & Quality Systems","item":"Tech transfer package & batch records","detail":"Process description, BOM, parameters, MBRs with appropriate IPC/acceptance criteria.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Regulatory (Module 3)","item":"3.2.S (Vector DS) & 3.2.P (DP) drafts","detail":"Describe materials, manufacturing, critical steps/intermediates; DP formulation & controls.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
    ],
    "Monoclonal Antibody (mAb)": [
        {"category":"Drug Substance","item":"Process description & flow diagram (UP/DS)","detail":"Cell line, upstream bioreactor, downstream capture/polish, UF/DF to bulk DS.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Substance","item":"Process control strategy (DS)","detail":"CPPs/IPC across UP/DS; raw materials strategy; impurity clearance claims.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Drug Product","item":"DP process & device/closure strategy","detail":"Formulation, fill/finish, container closure integrity; device compatibility (if applicable).","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Release/characterization panel","detail":"Identity, purity/aggregates, charge variants, glycan profile, potency, HCP/HCDNA, safety.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Method lifecycle & reference standard strategy","detail":"Phase-appropriate method qualification/validation; RS qualification/bridging.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Analytical","item":"Stability program (ICH)","detail":"Real-time/accelerated; photo/thermal if applicable; bracketing/matrixing rationale.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Manufacturing & Quality Systems","item":"PPQ & APV strategy (phase-appropriate)","detail":"Define pathway from Phase 1 controls to pivotal PPQ/APV; link to validation master plan.","phase":{"Pre-IND / IND-enabling":{"relevance":"recommended","rigor":"exploratory"},"Phase 1":{"relevance":"recommended","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
        {"category":"Regulatory (Module 3)","item":"3.2.S / 3.2.P drafts & justification packages","detail":"Align DS/DP narratives, specs/acceptance criteria, method validation, and comparability.","phase":{"Pre-IND / IND-enabling":{"relevance":"required","rigor":"exploratory"},"Phase 1":{"relevance":"required","rigor":"exploratory"},"Phase 2/3 (Pivotal)":{"relevance":"required","rigor":"qualified"},"BLA / MAA":{"relevance":"required","rigor":"validated"}}},
    ],
}

def build_dataframe(modality, stage):
    import pandas as pd
    rows = []
    for d in TEMPLATES[modality]:
        meta = d["phase"][stage]
        rows.append({
            "Category": d["category"],
            "Deliverable": d["item"],
            "Details": d["detail"],
            "Relevance": meta["relevance"],
            "Rigor": meta["rigor"],
            "Selected": meta["relevance"] == "required"
        })
    df = pd.DataFrame(rows)
    df["req_sort"] = df["Relevance"].map({"required":0,"recommended":1,"defer":2})
    return df.sort_values(["req_sort","Category","Deliverable"]).drop(columns=["req_sort"]).reset_index(drop=True)

with st.sidebar:
    st.header("Planner Settings")
    modality = st.selectbox("Modality", MODALITIES, index=0)
    stage = st.selectbox("Development Stage", STAGES, index=1)
    show_only_required = st.checkbox("Show only 'required' items", value=False)
    show_details = st.checkbox("Show details", value=True)

df = build_dataframe(modality, stage)
df_view = df[df["Relevance"]=="required"].copy() if show_only_required else df.copy()

st.subheader(f"Checklist · {modality} · {stage}")
counts = df_view["Relevance"].value_counts().to_dict()
st.caption(f"Required: {counts.get('required',0)} · Recommended: {counts.get('recommended',0)} · Defer: {counts.get('defer',0)}")

selected_rows = []
for cat, sub in df_view.groupby("Category"):
    with st.expander(cat, expanded=True):
        for i, r in sub.iterrows():
            c1, c2 = st.columns([0.06,0.94])
            with c1:
                chk = st.checkbox("", key=f"sel_{i}", value=bool(r["Selected"]))
            with c2:
                title = f"**{r['Deliverable']}**"
                if show_details and r["Details"]:
                    title += f"  \\n{r['Details']}"
                title += f"  \\n*Relevance:* `{r['Relevance']}` · *Rigor:* `{r['Rigor']}`"
                st.markdown(title)
            if chk:
                selected_rows.append(r)

import pandas as pd
export_df = pd.DataFrame(selected_rows) if selected_rows else df_view.copy()
export_df = export_df[["Category","Deliverable","Details","Relevance","Rigor"]]

st.markdown('---')
st.subheader("Export")

from io import StringIO
csv_buf = StringIO()
export_df.to_csv(csv_buf, index=False)
csv_bytes = csv_buf.getvalue().encode("utf-8")

md_lines = [f"# CMC Milestone Checklist — {modality} — {stage}", ""]
for _, r in export_df.iterrows():
    line = f"- **{r['Category']}** — **{r['Deliverable']}**"
    if show_details and r["Details"]:
        line += f": {r['Details']}"
    line += f" _(Relevance: {r['Relevance']}, Rigor: {r['Rigor']})_"
    md_lines.append(line)
md_bytes = "\\n".join(md_lines).encode("utf-8")

st.download_button("⬇️ Download CSV", data=csv_bytes, file_name=f"CMC_Milestones_{modality}_{stage}_{date.today().isoformat()}.csv", mime="text/csv", use_container_width=True)
st.download_button("⬇️ Download Markdown", data=md_bytes, file_name=f"CMC_Milestones_{modality}_{stage}_{date.today().isoformat()}.md", mime="text/markdown", use_container_width=True)
st.caption("Note: Phase-appropriate content is illustrative and should be adapted to your program/regulatory context.")
