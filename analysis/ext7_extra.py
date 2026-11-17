"""Extension 7, descriptive and exploratory part (section 5 of docs/preregistration_extension7.md). Nothing here is a
confirmatory test; those are in analysis.ext7.

  python -m analysis.ext7_extra -> results/ext7/ext4_new_models/, results/ext7/ext5_new_models/ (the frozen extension-4
                                   and extension-5 analyses on the six new models, Holm within these six),
                                   results/ext7/new_models_readings.csv, results/ext7/all_models.csv, results/ext7/extra.md

All models together: the eight family-G estimates for every model of the project that has the data (the nine Ada models on
the full banks; Qwen2.5-3B on the extension-4 bank; the two API models on the core subsets, which have no F module), against model size (Spearman correlation with log parameters).
"""
import numpy as np
import pandas as pd
from scipy import stats

from analysis import ext4, ext5, ext7
from analysis.common import md_table
from analysis.ext4 import EXT7_KEYS, LABEL
from config import RESULTS_DIR

OUT = RESULTS_DIR / "ext7"
META = {  # developer, parameters (billions), data
    "qwen25_3b": ("Alibaba", 3.1, "ext4 only"), "qwen25_7b": ("Alibaba", 7.6, "full"), "qwen25_14b": ("Alibaba", 14.8, "full"),
    "qwen38_27b": ("Alibaba", 27.0, "core subset"), "llama32_3b": ("Meta", 3.2, "full"), "llama31_8b": ("Meta", 8.0, "full"),
    "gemma3_4b": ("Google", 4.3, "full"), "gemma3_12b": ("Google", 12.2, "full"),
    "mistral_nemo_12b": ("Mistral AI", 12.2, "full"), "phi4_14b": ("Microsoft", 14.7, "full"),
    "granite33_8b": ("IBM", 8.2, "full"), "gptoss_120b": ("OpenAI", 117.0, "core subset"),
}
ADA = ["qwen25_7b", "llama31_8b", "qwen25_14b"] + EXT7_KEYS


def readings(res5):
    """The pre-specified readings of extension 5, applied to each new model."""
    r, rex, f, p, pdesc = res5["R"], res5["Rex"], res5["F"], res5["P"], res5["Pdesc"]
    rows = []
    for m in EXT7_KEYS:
        s = r[r.model_key == m].set_index("id")
        sup = rex[(rex.model == LABEL[m]) & (rex.test == "anger effect: suppression - filler")].est.iloc[0]
        if not s.loc["R1", "supported"]:
            reg = "no regulation"
        elif s.loc["R2", "supported"]:
            reg = "human-like"
        elif sup < 0:
            reg = "instruction following"
        else:
            reg = "reappraisal only"
        ff = f[f.model_key == m].iloc[0]
        pm = p[p.model_key == m].set_index("id")
        br = pdesc[(pdesc.model == LABEL[m]) & pdesc.message_set.isin(ext5.INJ) & (pdesc.defence != "none")]
        rows.append(dict(
            model=LABEL[m], anger_effect=s.loc["R0", "est"], anger_supported=bool(s.loc["R0", "supported"]),
            reappraisal_vs_filler=s.loc["R1", "est"], reappraisal_vs_suppression=s.loc["R2", "est"],
            suppression_vs_filler=sup, regulation_reading=reg,
            warning_effect=pm.loc["P1", "est"], warning_supported=bool(pm.loc["P1", "supported"]),
            reminder_effect=pm.loc["P2", "est"], reminder_supported=bool(pm.loc["P2", "supported"]),
            injection_sets_still_breaking=f"{int(br.still_breaks.sum())}/{len(br)}",
            mao_calm=100 * ff.mao_calm, mao_angry=100 * ff.mao_angry, mao_supported=bool(ff.supported),
            identified=bool(ff.identified), beta_calm=ff.beta_calm, beta_angry=ff.beta_angry,
            beta_identified=bool(ff.beta_identified)))
    return pd.DataFrame(rows)


def all_models():
    gm, ge = ext7.g_models(models=ADA + ["qwen25_3b"])
    api, _ = ext7.g_models(models=["qwen38_27b", "gptoss_120b"])  # core subsets: no F module, so no G7/G8
    t = pd.concat([gm, api], ignore_index=True)
    w = t.pivot(index="model_key", columns="id", values="est").reset_index()
    w.insert(0, "model", w.model_key.map(lambda k: LABEL.get(k, k)))
    w.insert(1, "developer", w.model_key.map(lambda k: META[k][0]))
    w.insert(2, "params_B", w.model_key.map(lambda k: META[k][1]))
    w.insert(3, "data", w.model_key.map(lambda k: META[k][2]))
    w = w.sort_values("params_B").reset_index(drop=True)
    size = []
    for hid, label, alt, mu0 in ext7.G_SPECS:
        d = w[["params_B", hid]].dropna()
        rho, p = stats.spearmanr(np.log(d.params_B), d[hid])
        sign = (d[hid] - mu0 > 0) if alt == "greater" else (d[hid] - mu0 < 0)
        size.append(dict(id=hid, finding=label, models=len(d), predicted_sign=f"{int(sign.sum())}/{len(d)}",
                         median=d[hid].median(), min=d[hid].min(), max=d[hid].max(), spearman_rho_log_size=rho, p=p))
    return w, pd.DataFrame(size), ge


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ext4.report(out=OUT / "ext4_new_models", models=EXT7_KEYS)
    res5 = ext5.report(out=OUT / "ext5_new_models", models=EXT7_KEYS)
    rd = readings(res5)
    w, size, _ = all_models()
    rd.to_csv(OUT / "new_models_readings.csv", index=False)
    w.to_csv(OUT / "all_models.csv", index=False)
    size.to_csv(OUT / "all_models_size.csv", index=False)
    L = ["# Extension 7: descriptive and exploratory tables", "",
         "Section 5 of `docs/preregistration_extension7.md`. Nothing here is a confirmatory test. The full per-model tests of "
         "the six new models (Holm within these six) are in `ext4_new_models/report.md` and `ext5_new_models/report.md`.", "",
         "## The pre-specified readings of extension 5, for each new model", "",
         "Estimates in percentage points; MAO\\* in % of the pie. `regulation_reading`: human-like = R1 and R2 supported; "
         "instruction following = R1 supported, R2 not, suppression - filler negative; no regulation = R1 not supported.", "",
         md_table(rd.round(2)), "",
         "## All models of the project (exploratory)", "",
         "G1 fake SYSTEM notice - neutral (share handed over); G2 rejection of a 100% offer (%); G3 anger effect on rejection; "
         "G4 reappraisal - filler; G5 suppression - filler; G6 reminder defence; G7 anger effect on MAO\\*; G8 anger effect on "
         "accepting offers above 50%. API models ran the core subsets.", "",
         md_table(w.drop(columns="model_key").round(1)), "",
         "Against model size (Spearman correlation with log parameters; models differ in more than size):", "",
         md_table(size.round(3)), ""]
    (OUT / "extra.md").write_text("\n".join(L), encoding="utf-8")
    print(OUT / "extra.md")
    print(rd.round(1).to_string())
    print(w.drop(columns="model_key").round(1).to_string())
    print(size.round(3).to_string())


if __name__ == "__main__":
    main()
