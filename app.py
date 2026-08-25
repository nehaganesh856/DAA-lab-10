import streamlit as st
import math
import pandas as pd

# ---------------------------------------------------
# First Fit
# ---------------------------------------------------

def first_fit(items, capacity=1.0):
    bins = []
    bin_contents = []

    for item in items:
        placed = False

        for i, space in enumerate(bins):
            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------------------------------------------
# First Fit Decreasing
# ---------------------------------------------------

def first_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)
    return first_fit(sorted_items, capacity)


# ---------------------------------------------------
# Best Fit Decreasing
# ---------------------------------------------------

def best_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            if space >= item and space - item < best_space:
                best_space = space - item
                best_idx = i

        if best_idx >= 0:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)

        else:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------------------------------------------
# Display bin information
# ---------------------------------------------------

def get_bin_data(bins, capacity):

    data = []

    for i, b in enumerate(bins, 1):

        used = sum(b)
        remaining = capacity - used
        utilization = (used / capacity) * 100

        data.append({
            "Bin": f"Bin {i}",
            "Items": ", ".join(
                str(round(x, 2)) for x in b
            ),
            "Used": round(used, 2),
            "Remaining": round(remaining, 2),
            "Utilization": round(utilization, 1)
        })

    return data


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Bin Packing Algorithms",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("📦 Bin Packing Problem")

st.write(
    "Compare three bin packing heuristics: "
    "**First Fit (FF), First Fit Decreasing (FFD), "
    "and Best Fit Decreasing (BFD).**"
)

st.divider()


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.header("⚙️ Input Settings")

capacity = st.sidebar.number_input(
    "Bin Capacity",
    min_value=0.1,
    max_value=100.0,
    value=1.0,
    step=0.1
)

items_input = st.sidebar.text_area(
    "Enter Items",
    value="0.5, 0.7, 0.3, 0.9, 0.2, 0.6, 0.8, 0.4, 0.1, 0.5",
    help="Enter item sizes separated by commas."
)


# ---------------------------------------------------
# Parse Items
# ---------------------------------------------------

try:

    items = [
        float(x.strip())
        for x in items_input.split(",")
        if x.strip()
    ]

except ValueError:

    st.error(
        "❌ Invalid input. Please enter numbers separated by commas."
    )

    st.stop()


# Validate items

if not items:

    st.warning("Please enter at least one item.")
    st.stop()

if any(x <= 0 for x in items):

    st.error("❌ Item sizes must be greater than 0.")
    st.stop()

if any(x > capacity for x in items):

    st.error(
        "❌ Every item must be smaller than or equal to the bin capacity."
    )

    st.stop()


# ---------------------------------------------------
# Input Summary
# ---------------------------------------------------

st.subheader("📋 Input Information")

col1, col2, col3, col4 = st.columns(4)

total_size = sum(items)

lower_bound = math.ceil(total_size / capacity)

with col1:
    st.metric(
        "Number of Items",
        len(items)
    )

with col2:
    st.metric(
        "Bin Capacity",
        f"{capacity:.2f}"
    )

with col3:
    st.metric(
        "Total Item Size",
        f"{total_size:.2f}"
    )

with col4:
    st.metric(
        "Lower Bound",
        lower_bound
    )


st.write("**Items:**", items)

st.divider()


# ---------------------------------------------------
# Run Algorithms
# ---------------------------------------------------

ff_bins = first_fit(items, capacity)
ffd_bins = first_fit_decreasing(items, capacity)
bfd_bins = best_fit_decreasing(items, capacity)


# ---------------------------------------------------
# Summary
# ---------------------------------------------------

st.subheader("📊 Algorithm Comparison")

comparison = pd.DataFrame({
    "Algorithm": [
        "First Fit (FF)",
        "First Fit Decreasing (FFD)",
        "Best Fit Decreasing (BFD)"
    ],
    "Number of Bins": [
        len(ff_bins),
        len(ffd_bins),
        len(bfd_bins)
    ]
})

comparison["Extra Bins Above Lower Bound"] = (
    comparison["Number of Bins"] - lower_bound
)

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------
# Best Result
# ---------------------------------------------------

results = {
    "First Fit (FF)": len(ff_bins),
    "First Fit Decreasing (FFD)": len(ffd_bins),
    "Best Fit Decreasing (BFD)": len(bfd_bins)
}

best_algorithm = min(
    results,
    key=results.get
)

best_bin_count = results[best_algorithm]

if best_bin_count == lower_bound:

    st.success(
        f"🏆 **{best_algorithm}** achieved the theoretical lower bound "
        f"of {lower_bound} bins!"
    )

else:

    st.info(
        f"🏆 Best result: **{best_algorithm}** "
        f"using {best_bin_count} bins."
    )


st.divider()


# ---------------------------------------------------
# Bin Visualization Function
# ---------------------------------------------------

def display_bins_streamlit(
    label,
    bins,
    capacity
):

    st.subheader(label)

    st.write(
        f"**Total bins:** {len(bins)}"
    )

    for i, bin_items in enumerate(bins, 1):

        used = sum(bin_items)
        remaining = capacity - used
        utilization = used / capacity

        st.write(
            f"**Bin {i}** — "
            f"Used: `{used:.2f}` / `{capacity:.2f}` "
            f"({utilization * 100:.1f}%)"
        )

        st.progress(
            min(utilization, 1.0)
        )

        st.caption(
            f"Items: {[round(x, 2) for x in bin_items]} "
            f"| Remaining: {remaining:.2f}"
        )


# ---------------------------------------------------
# Tabs
# ---------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "🟦 First Fit",
    "🟩 First Fit Decreasing",
    "🟧 Best Fit Decreasing"
])


with tab1:

    display_bins_streamlit(
        "First Fit (FF)",
        ff_bins,
        capacity
    )

    st.dataframe(
        pd.DataFrame(
            get_bin_data(ff_bins, capacity)
        ),
        use_container_width=True,
        hide_index=True
    )


with tab2:

    display_bins_streamlit(
        "First Fit Decreasing (FFD)",
        ffd_bins,
        capacity
    )

    st.dataframe(
        pd.DataFrame(
            get_bin_data(ffd_bins, capacity)
        ),
        use_container_width=True,
        hide_index=True
    )


with tab3:

    display_bins_streamlit(
        "Best Fit Decreasing (BFD)",
        bfd_bins,
        capacity
    )

    st.dataframe(
        pd.DataFrame(
            get_bin_data(bfd_bins, capacity)
        ),
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------
# Detailed Comparison
# ---------------------------------------------------

st.divider()

st.subheader("📈 Detailed Comparison")

detail_data = []

for name, bins in [
    ("First Fit (FF)", ff_bins),
    ("First Fit Decreasing (FFD)", ffd_bins),
    ("Best Fit Decreasing (BFD)", bfd_bins)
]:

    total_used = sum(sum(b) for b in bins)
    total_capacity = len(bins) * capacity
    utilization = (
        total_used / total_capacity
    ) * 100

    detail_data.append({
        "Algorithm": name,
        "Bins Used": len(bins),
        "Total Capacity": round(total_capacity, 2),
        "Used Space": round(total_used, 2),
        "Unused Space": round(
            total_capacity - total_used,
            2
        ),
        "Average Utilization (%)": round(
            utilization,
            2
        )
    })


detail_df = pd.DataFrame(detail_data)

st.dataframe(
    detail_df,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.divider()

st.caption(
    "Bin Packing Problem | First Fit | "
    "First Fit Decreasing | Best Fit Decreasing"
)
