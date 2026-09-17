import streamlit as st
import pandas as pd

st.set_page_config(page_title="Builderr Community Assistant", page_icon="🛠️", layout="wide")

st.title("🛠️ Builderr Community Assistant — Human Review Dashboard")
st.caption("Reviewing drafted community responses prior to approval.")

try:
    df = pd.read_csv("results.csv")
    df_raw = pd.read_csv("sample_posts.csv")
    merged = pd.merge(df, df_raw, on="post_id")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Posts Evaluated", len(merged))
    col2.metric("Drafts Generated", len(merged[merged["should_respond"] == "Yes"]))
    
    st.divider()
    for _, row in merged.iterrows():
        status = " YES - RESPOND" if row["should_respond"] == "Yes" else " NO - SKIP"
        with st.expander(f"Post {row['post_id']} | {row['community']} — {status}"):
            st.markdown(f"**Post Summary:** {row['post_summary']}")
            st.markdown(f"**Community Context:** {row['community_context']}")
            st.markdown(f"**Rationale:** {row['why']}")
            if row["should_respond"] == "Yes":
                st.success(f"**Draft Response:**\n\n{row['draft_response']}")
            else:
                st.info("No response drafted (prevents spam / respects community norms).")
except Exception as e:
    st.info("Run assistant.py to generate results.csv first.")