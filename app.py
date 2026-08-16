import streamlit as st
from datetime import date
import logging

logger = logging.getLogger(__name__)

from run import main as run_pipeline
from src.database import get_stock_data
from src.queries import get_daily_change
import src.config as config
from src.ingestion import APIError


TICKER = config.TICKER
CHUNK_SIZE = 200


# Titles
# -------------------------------------------------------------------
st.set_page_config(
    page_title=f"{TICKER} Stock Data",
    layout="wide"
)

st.title(f"{TICKER} Stock Data")
st.caption(f"Data shown for {date.today().strftime('%d %B %Y')}")


# Refresh
# -------------------------------------------------------------------

def refresh_data():
    with st.spinner("Updating stock data..."):
        try:
            run_pipeline()

        except APIError:
            st.error(
                "Unable to refresh stock data right now. "
                "Please try again later."
            )

        except Exception:
            logger.exception("Unexpected pipeline failure")

            st.error(
                "An unexpected error occurred while refreshing the data."
            )

        else:
            st.success("Data refreshed successfully.")
            st.rerun()


# Run pipeline on startup
if "initialised" not in st.session_state:
    st.session_state.initialised = True
    refresh_data()

# Refresh data with button
if st.button("Refresh data"):
    refresh_data()




# Latest price / daily change
# -------------------------------------------------------------------

daily_change = get_daily_change(TICKER)

latest_close = daily_change["latest_close"]
absolute_change = daily_change["absolute_change"]
percentage_change = daily_change["percentage_change"]


col1, col2 = st.columns(2)


with col1:
    st.metric(
        label="Latest Close",
        value=f"${latest_close:.2f}" if latest_close is not None else "N/A"
    )


with col2:
    if absolute_change is None or percentage_change is None:
        st.metric(
            label="Daily Change",
            value="N/A"
        )
    else:
        st.metric(
            label="Daily Change",
            value=f"${absolute_change:+.2f}",
            delta=f"{percentage_change:+.2f}%"
        )



# Historical data
# -------------------------------------------------------------------

st.subheader("Historical Data")


if "rows_to_show" not in st.session_state:
    st.session_state["rows_to_show"] = CHUNK_SIZE


rows_to_show = st.session_state["rows_to_show"]

stock_data = get_stock_data(
    ticker=TICKER,
    limit=rows_to_show,
    offset=0
)


st.dataframe(
    stock_data,
    width="stretch",
    height=600,
    hide_index=True,
    column_config={
        "open": st.column_config.NumberColumn(
            "Open",
            format="$%.2f"
        ),
        "high": st.column_config.NumberColumn(
            "High",
            format="$%.2f"
        ),
        "low": st.column_config.NumberColumn(
            "Low",
            format="$%.2f"
        ),
        "close": st.column_config.NumberColumn(
            "Close",
            format="$%.2f"
        ),
        "volume": st.column_config.NumberColumn(
            "Volume",
            format="%,d"
        )
    }
)

# Load more
# -------------------------------------------------------------------

if len(stock_data) == rows_to_show:

    if st.button("Load 200 more rows"):
        st.session_state["rows_to_show"] += CHUNK_SIZE
        st.rerun()