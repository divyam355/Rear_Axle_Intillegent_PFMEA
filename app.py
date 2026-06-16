import streamlit as st
import pandas as pd
from PIL import Image

logo = Image.open(
    "images/logo.png"
)

st.sidebar.image(
    logo,
    use_container_width=True
)
banner = Image.open(
    "images/dashboard_banner.png"
)

st.image(
    banner,
    use_container_width=True
)

import os
from datetime import datetime

st.set_page_config(
    page_title="Rear Axle Intelligent PFMEA",
    layout="wide"
)
housing_pfmea = pd.read_csv(
    "data/housing_pfmea.csv"
)
drive_head_pfmea = pd.read_csv(
    "data/drive_head_pfmea.csv"
)
wheel_end_pfmea = pd.read_csv(
    "data/wheel_end_pfmea.csv"
)
shaft_pfmea = pd.read_csv(
    "data/shaft_pfmea.csv"
)
brake_pfmea = pd.read_csv(
    "data/brake_pfmea.csv"
)
df = pd.read_csv("data/failure_log.csv")

st.write("Shape:", df.shape)
st.write(df.head())
from datetime import datetime

def log_failure(
    module,
    process,
    location,
    failure_mode,
    rpn
):

    new_record = pd.DataFrame([{

        "Date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Module": module,

        "Process": process,

        "Location": location,

        "FailureMode": failure_mode,

        "RPN": rpn

    }])

    new_record.to_csv(
        "data/failure_log.csv",
        mode="a",
        header=False,
        index=False
    )
st.title("🏭 Rear Axle Intelligent PFMEA Platform")

module = st.sidebar.selectbox(
    "Select Module",
    [
        "Housing Module",
        "Drive Head Module",
        "Wheel End Module",
        "Shaft Module",
        "Brake Module",
        "Master PFMEA Dashboard"

    ]
)

# ==========================================
# HOUSING MODULE
# ==========================================

if module == "Housing Module":

    st.header("Housing Module")

    process = st.selectbox(
        "Select Process",
        [
            "Drain Plug Assembly",
            "Magnetic Plug Assembly"
        ]
    )

    st.divider()

    plug_present = st.selectbox(
        "Plug Present?",
        ["Yes", "No"]
    )

    washer_present = st.selectbox(
        "Washer Present?",
        ["Yes", "No"]
    )

    torque = st.number_input(
        "Enter Torque Value (Nm)",
        min_value=0.0,
        step=0.1
    )

    if st.button("Evaluate"):
        target = 35

        min_limit = 33.25
        max_limit = 36.75

        failures = []

        if plug_present == "No":
            failures.append({
                "location": process,
                "failure": "Missing Plug"
            })

            st.error("❌ Missing Plug")

        if washer_present == "No":
            failures.append({
                "location": process,
                "failure": "Missing Washer"
            })

            st.error("❌ Missing Washer")

        if torque < min_limit:
            failures.append({
                "location": process,
                "failure": "Under Torque"
            })

            st.warning("🟡 UNDER TORQUE")

        if torque > max_limit:
            failures.append({
                "location": process,
                "failure": "Over Torque"
            })

            st.error("🔴 OVER TORQUE")

        if len(failures) == 0:
            st.success("🟢 ASSEMBLY OK")

        st.write("Target Torque:", target)
        st.write("Minimum Limit:", min_limit)
        st.write("Maximum Limit:", max_limit)

        for item in failures:

            location = item["location"]
            failure_mode = item["failure"]

            pfmea_record = housing_pfmea[
                (housing_pfmea["Process"] == process)
                &
                (housing_pfmea["FailureMode"] == failure_mode)
                ]

            if not pfmea_record.empty:

                row = pfmea_record.iloc[0]

                severity = row["Severity"]
                occurrence = row["Occurrence"]
                detection = row["Detection"]

                rpn = severity * occurrence * detection
                log_failure(
                    module="Housing",
                    process="Housing",
                    location=item["location"],
                    failure_mode=row["FailureMode"],
                    rpn=rpn
                )

                st.divider()

                st.subheader(
                    f"PFMEA Analysis - {location}"
                )

                st.write("Failure Mode:", row["FailureMode"])
                st.write("Failure Effect:", row["FailureEffect"])
                st.write("Failure Cause:", row["FailureCause"])
                st.write("Severity:", severity)
                st.write("Occurrence:", occurrence)
                st.write("Detection:", detection)
                st.write("RPN:", rpn)

                if rpn < 50:
                    st.success("🟢 Risk Level: LOW")

                elif rpn < 100:
                    st.warning("🟡 Risk Level: MEDIUM")

                else:
                    st.error("🔴 Risk Level: HIGH")

# ==================================================
# DRIVE HEAD MODULE
# ==================================================

if module == "Drive Head Module":

    st.header("⚙️ Drive Head Module")

    process = st.selectbox(
        "Select Process",
        [
            "Sealant Application",
            "Drive Head Fitment",
            "Drive Head Bolt Tightening"
        ]
    )

    st.divider()

    failures = []

    # -----------------------------------
    # Sealant Application
    # -----------------------------------

    if process == "Sealant Application":

        sealant = st.selectbox(
            "Sealant Applied?",
            ["Yes", "No"]
        )

        if st.button("Evaluate Drive Head"):

            if sealant == "No":

                failures.append({
                    "bolt": "Sealant Application",
                    "failure": "Sealant Missing"
                })

                st.error(
                    "❌ Sealant Missing"
                )

            else:

                st.success(
                    "🟢 Sealant OK"
                )

    # -----------------------------------
    # Drive Head Fitment
    # -----------------------------------
    elif process == "Drive Head Fitment":

        seating = st.selectbox(
            "Proper Seating?",
            ["Yes", "No"]
        )

        if st.button("Evaluate Drive Head"):

            failures = []

            if seating == "No":

                failures.append({
                    "location": "Drive Head Fitment",
                    "failure": "Improper Seating"
                })

                st.error(
                    "❌ Improper Seating"
                )

            else:

                st.success(
                    "🟢 Fitment OK"
                )

            for item in failures:

                pfmea_record = drive_head_pfmea[
                    (drive_head_pfmea["Process"] == "Drive Head Fitment")
                    &
                    (drive_head_pfmea["FailureMode"] == item["failure"])
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    rpn = (
                            row["Severity"]
                            *
                            row["Occurrence"]
                            *
                            row["Detection"]
                    )

                    log_failure(
                        module="Drive Head",
                        process="Drive Head Fitment",
                        location="Drive Head Fitment",
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        "PFMEA Analysis - Drive Head Fitment"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
                    if rpn < 50:

                        st.success(
                            "🟢 Risk Level: LOW"
                        )

                    elif rpn < 100:

                        st.warning(
                            "🟡 Risk Level: MEDIUM"
                        )

                    else:

                        st.error(
                            "🔴 Risk Level: HIGH"
                        )

    # -----------------------------------
    # Bolt Tightening
    # -----------------------------------

    elif process == "Drive Head Bolt Tightening":

        st.subheader("Drive Head Torque Traceability")

        target = 180

        min_limit = 171

        max_limit = 189

        st.info(

            f"Target Torque = {target} Nm | "

            f"Min = {min_limit} Nm | "

            f"Max = {max_limit} Nm"

        )

        bolt_inputs = []

        h1, h2, h3 = st.columns([1, 1, 1])

        with h1:
            st.markdown("### Bolt No")

        with h2:
            st.markdown("### Present")

        with h3:
            st.markdown("### Torque (Nm)")

        present_list = []
        torque_list = []

        for i in range(12):
            c1, c2, c3 = st.columns([1, 1, 1])

            with c1:
                st.write(f"Bolt {i + 1}")

            with c2:
                present = st.selectbox(
                    f"Present {i + 1}",
                    ["Yes", "No"],
                    index=0,
                    label_visibility="collapsed",
                    key=f"present_{i}"
                )

                present_list.append(present)

            with c3:
                torque = st.number_input(
                    f"Torque {i + 1}",
                    min_value=0.0,
                    step=0.1,
                    label_visibility="collapsed",
                    key=f"torque_{i}"
                )

                torque_list.append(torque)
        if st.button("Evaluate Drive Head"):

            results = []

            ok_count = 0

            under_count = 0

            over_count = 0

            missing_count = 0

            failures = []

            for i in range(12):

                present = present_list[i]

                torque = torque_list[i]

                if present == "No":

                    status = "⚫ MISSING BOLT"

                    missing_count += 1

                    failures.append({
                        "bolt": f"Bolt {i + 1}",
                        "failure": "Missing Bolt"
                    })


                elif torque < min_limit:

                    status = "🟡 UNDER TORQUE"

                    under_count += 1

                    failures.append({
                        "bolt": f"Bolt {i + 1}",
                        "failure": "Under Torque"
                    })


                elif torque > max_limit:

                    status = "🔴 OVER TORQUE"

                    over_count += 1

                    failures.append({
                        "bolt": f"Bolt {i + 1}",
                        "failure": "Over Torque"
                    })


                else:

                    status = "🟢 OK"

                    ok_count += 1

                results.append([

                    f"Bolt {i + 1}",

                    present,

                    torque,

                    status

                ])

            total_bolts = 12

            compliance = round(

                (ok_count / total_bolts) * 100,

                2

            )

            st.divider()

            k1, k2, k3, k4, k5 = st.columns(5)

            k1.metric(

                "Total Bolts",

                total_bolts

            )

            k2.metric(

                "OK",

                ok_count

            )

            k3.metric(

                "Missing",

                missing_count

            )

            k4.metric(

                "Under",

                under_count

            )

            k5.metric(

                "Over",

                over_count

            )

            st.metric(

                "Compliance %",

                compliance

            )

            result_df = pd.DataFrame(

                results,

                columns=[

                    "Bolt No",

                    "Present",

                    "Torque (Nm)",

                    "Status"

                ]

            )

            st.dataframe(

                result_df,

                use_container_width=True


            )
    # -----------------------------------
    # -----------------------------------
    # PFMEA ANALYSIS
    # -----------------------------------

    unique_failures = []

    for item in failures:

        if item not in unique_failures:
            unique_failures.append(item)

    for item in failures:

        pfmea_record = drive_head_pfmea[
            (drive_head_pfmea["Process"] == "Sealant Application")
            &
            (drive_head_pfmea["FailureMode"] == item["failure"])
            ]

        if not pfmea_record.empty:

            row = pfmea_record.iloc[0]

            rpn = (
                    row["Severity"]
                    *
                    row["Occurrence"]
                    *
                    row["Detection"]
            )

            st.divider()

            st.subheader(
                "PFMEA Analysis - Sealant Application"
            )

            st.write(
                "Failure Mode:",
                row["FailureMode"]
            )

            st.write(
                "Failure Effect:",
                row["FailureEffect"]
            )

            st.write(
                "Failure Cause:",
                row["FailureCause"]
            )

            st.write(
                "RPN:",
                rpn
            )

            if rpn < 50:

                st.success(
                    "🟢 Risk Level: LOW"
                )

            elif rpn < 100:

                st.warning(
                    "🟡 Risk Level: MEDIUM"
                )

            else:

                st.error(
                    "🔴 Risk Level: HIGH"
                )
# ==================================================
# WHEEL END MODULE
# ==================================================

if module == "Wheel End Module":

    st.header("🛞 Wheel End Module")

    side = st.selectbox(
        "Select Side",
        [
            "RH Wheel End",
            "LH Wheel End"
        ]
    )

    assembly = st.selectbox(
        "Select Assembly",
        [
            "Pole Wheel Assembly",
            "Brake Disc Assembly",
            "Wheel Hub Assembly",
            "Chuck Nut Assembly"
        ]
    )

    if assembly == "Wheel Hub Assembly":

        st.subheader(
            f"{side} - Wheel Hub Nut Tightening"
        )

        target = 450

        min_limit = 427.5
        max_limit = 472.5

        st.info(
            f"Target Torque = {target} Nm | "
            f"Min = {min_limit} Nm | "
            f"Max = {max_limit} Nm"
        )

        h1, h2, h3 = st.columns([1, 1, 1])

        with h1:
            st.markdown("### Nut No")

        with h2:
            st.markdown("### Present")

        with h3:
            st.markdown("### Torque")

        present_list = []
        torque_list = []

        for i in range(6):
            c1, c2, c3 = st.columns([1, 1, 1])

            with c1:
                st.write(f"Nut {i + 1}")

            with c2:
                present = st.selectbox(
                    f"Present {i}",
                    ["Yes", "No"],
                    index=0,
                    label_visibility="collapsed",
                    key=f"wh_present_{i}"
                )

                present_list.append(present)

            with c3:
                torque = st.number_input(
                    f"Torque {i}",
                    min_value=0.0,
                    step=0.1,
                    label_visibility="collapsed",
                    key=f"wh_torque_{i}"
                )

                torque_list.append(torque)

        if st.button("Evaluate Wheel Hub"):

            failures = []

            results = []

            ok_count = 0
            under_count = 0
            over_count = 0
            missing_count = 0

            for i in range(6):

                present = present_list[i]
                torque = torque_list[i]

                if present == "No":

                    status = "⚫ MISSING NUT"

                    missing_count += 1

                    failures.append({
                        "location": f"Nut {i + 1}",
                        "failure": "Missing Nut"
                    })

                elif torque < min_limit:

                    status = "🟡 UNDER TORQUE"

                    under_count += 1

                    failures.append({
                        "location": f"Nut {i + 1}",
                        "failure": "Under Torque"
                    })

                elif torque > max_limit:

                    status = "🔴 OVER TORQUE"

                    over_count += 1

                    failures.append({
                        "location": f"Nut {i + 1}",
                        "failure": "Over Torque"
                    })

                else:

                    status = "🟢 OK"

                    ok_count += 1

                results.append([
                    f"Nut {i + 1}",
                    present,
                    torque,
                    status
                ])

            st.divider()

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric("Total", 6)
            c2.metric("OK", ok_count)
            c3.metric("Missing", missing_count)
            c4.metric("Under", under_count)
            c5.metric("Over", over_count)

            result_df = pd.DataFrame(
                results,
                columns=[
                    "Nut",
                    "Present",
                    "Torque",
                    "Status"
                ]
            )

            st.dataframe(
                result_df,
                use_container_width=True
            )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = wheel_end_pfmea[
                    (wheel_end_pfmea["Process"] == "Wheel Hub Nut Tightening")
                    &
                    (wheel_end_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    severity = row["Severity"]
                    occurrence = row["Occurrence"]
                    detection = row["Detection"]

                    rpn = (
                            severity *
                            occurrence *
                            detection
                    )
                    log_failure(
                        module="Wheel End",
                        process="Wheel Hub Nut Tightning",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
    elif assembly == "Pole Wheel Assembly":

        st.subheader(
            f"{side} - Pole Wheel Assembly"
        )

        failures = []

        pole_wheel = st.selectbox(
            "Pole Wheel Present?",
            ["Yes", "No"]
        )

        if pole_wheel == "No":
            failures.append({
                "location": "Pole Wheel Assembly",
                "failure": "Pole Wheel Missing"
            })

            st.error("❌ Pole Wheel Missing")

        st.divider()

        st.markdown("### Washer Verification")

        washer_status = []

        for i in range(4):

            washer = st.selectbox(
                f"Washer {i + 1} Present?",
                ["Yes", "No"],
                key=f"pw_washer_{i}"
            )

            washer_status.append(washer)

            if washer == "No":
                failures.append({
                    "location": f"Washer {i + 1}",
                    "failure": "Washer Missing"
                })

        st.divider()

        st.markdown("### Bolt Torque Traceability")

        target = 25
        min_limit = 23.75
        max_limit = 26.25

        st.info(
            f"Target Torque = {target} Nm | "
            f"Min = {min_limit} Nm | "
            f"Max = {max_limit} Nm"
        )

        h1, h2, h3 = st.columns([1, 1, 1])

        with h1:
            st.markdown("### Bolt No")

        with h2:
            st.markdown("### Present")

        with h3:
            st.markdown("### Torque")

        present_list = []
        torque_list = []

        for i in range(4):
            c1, c2, c3 = st.columns([1, 1, 1])

            with c1:
                st.write(f"Bolt {i + 1}")

            with c2:
                present = st.selectbox(
                    f"Present {i}",
                    ["Yes", "No"],
                    index=0,
                    label_visibility="collapsed",
                    key=f"pw_present_{i}"
                )

                present_list.append(present)

            with c3:
                torque = st.number_input(
                    f"Torque {i}",
                    min_value=0.0,
                    step=0.1,
                    label_visibility="collapsed",
                    key=f"pw_torque_{i}"
                )

                torque_list.append(torque)

        if st.button("Evaluate Pole Wheel"):

            results = []

            for i in range(4):

                present = present_list[i]
                torque = torque_list[i]

                if present == "No":

                    status = "⚫ MISSING BOLT"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Bolt Missing"
                    })

                elif torque < min_limit:

                    status = "🟡 UNDER TORQUE"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Under Torque"
                    })

                elif torque > max_limit:

                    status = "🔴 OVER TORQUE"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Over Torque"
                    })

                else:

                    status = "🟢 OK"

                results.append([
                    f"Bolt {i + 1}",
                    present,
                    torque,
                    status
                ])

            result_df = pd.DataFrame(
                results,
                columns=[
                    "Bolt",
                    "Present",
                    "Torque",
                    "Status"
                ]
            )

            st.dataframe(
                result_df,
                use_container_width=True
            )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = wheel_end_pfmea[
                    (wheel_end_pfmea["Process"] == "Pole Wheel Assembly")
                    &
                    (wheel_end_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    severity = row["Severity"]
                    occurrence = row["Occurrence"]
                    detection = row["Detection"]

                    rpn = (
                            severity *
                            occurrence *
                            detection
                    )
                    log_failure(
                        module="Wheel End",
                        process="Pole Wheel",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "Severity:",
                        severity
                    )

                    st.write(
                        "Occurrence:",
                        occurrence
                    )

                    st.write(
                        "Detection:",
                        detection
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
    elif assembly == "Brake Disc Assembly":

        st.subheader(
            f"{side} - Brake Disc Assembly"
        )

        target = 220

        min_limit = 209
        max_limit = 231

        st.info(
            f"Target Torque = {target} Nm | "
            f"Min = {min_limit} Nm | "
            f"Max = {max_limit} Nm"
        )

        h1, h2, h3 = st.columns([1, 1, 1])

        with h1:
            st.markdown("### Bolt No")

        with h2:
            st.markdown("### Present")

        with h3:
            st.markdown("### Torque")

        present_list = []
        torque_list = []

        for i in range(12):
            c1, c2, c3 = st.columns([1, 1, 1])

            with c1:
                st.write(f"Bolt {i + 1}")

            with c2:
                present = st.selectbox(
                    f"BD Present {i}",
                    ["Yes", "No"],
                    index=0,
                    label_visibility="collapsed",
                    key=f"bd_present_{i}"
                )

                present_list.append(present)

            with c3:
                torque = st.number_input(
                    f"BD Torque {i}",
                    min_value=0.0,
                    step=0.1,
                    label_visibility="collapsed",
                    key=f"bd_torque_{i}"
                )

                torque_list.append(torque)

        if st.button("Evaluate Brake Disc"):

            failures = []

            results = []

            for i in range(12):

                present = present_list[i]
                torque = torque_list[i]

                if present == "No":

                    status = "⚫ MISSING BOLT"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Missing Bolt"
                    })

                elif torque < min_limit:

                    status = "🟡 UNDER TORQUE"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Under Torque"
                    })

                elif torque > max_limit:

                    status = "🔴 OVER TORQUE"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Over Torque"
                    })

                else:

                    status = "🟢 OK"

                results.append([
                    f"Bolt {i + 1}",
                    present,
                    torque,
                    status
                ])

            result_df = pd.DataFrame(
                results,
                columns=[
                    "Bolt",
                    "Present",
                    "Torque",
                    "Status"
                ]
            )

            st.dataframe(
                result_df,
                use_container_width=True
            )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = wheel_end_pfmea[
                    (wheel_end_pfmea["Process"] == "Brake Disc Assembly")
                    &
                    (wheel_end_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    severity = row["Severity"]
                    occurrence = row["Occurrence"]
                    detection = row["Detection"]

                    rpn = (
                            severity *
                            occurrence *
                            detection
                    )
                    log_failure(
                        module="Wheel End",
                        process="Brake Disc",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "Severity:",
                        severity
                    )

                    st.write(
                        "Occurrence:",
                        occurrence
                    )

                    st.write(
                        "Detection:",
                        detection
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
    elif assembly == "Chuck Nut Assembly":

        st.subheader(
            f"{side} - Chuck Nut Assembly"
        )

        failures = []

        chuck_nut = st.selectbox(
            "Chuck Nut Present?",
            ["Yes", "No"]
        )

        washer = st.selectbox(
            "Washer Present?",
            ["Yes", "No"]
        )

        if chuck_nut == "No":
            failures.append({
                "location": "Chuck Nut Assembly",
                "failure": "Chuck Nut Missing"
            })

            st.error("❌ Chuck Nut Missing")

        if washer == "No":
            failures.append({
                "location": "Washer",
                "failure": "Washer Missing"
            })

            st.error("❌ Washer Missing")

        st.divider()

        target = 35

        min_limit = 33.25
        max_limit = 36.75

        st.info(
            f"Target Torque = {target} Nm | "
            f"Min = {min_limit} Nm | "
            f"Max = {max_limit} Nm"
        )

        h1, h2, h3 = st.columns([1, 1, 1])

        with h1:
            st.markdown("### Bolt No")

        with h2:
            st.markdown("### Present")

        with h3:
            st.markdown("### Torque")

        present_list = []
        torque_list = []

        for i in range(10):
            c1, c2, c3 = st.columns([1, 1, 1])

            with c1:
                st.write(f"Bolt {i + 1}")

            with c2:
                present = st.selectbox(
                    f"CN Present {i}",
                    ["Yes", "No"],
                    index=0,
                    label_visibility="collapsed",
                    key=f"cn_present_{i}"
                )

                present_list.append(present)

            with c3:
                torque = st.number_input(
                    f"CN Torque {i}",
                    min_value=0.0,
                    step=0.1,
                    label_visibility="collapsed",
                    key=f"cn_torque_{i}"
                )

                torque_list.append(torque)

        if st.button("Evaluate Chuck Nut"):

            results = []

            for i in range(10):

                present = present_list[i]
                torque = torque_list[i]

                if present == "No":

                    status = "⚫ MISSING BOLT"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Missing Bolt"
                    })

                elif torque < min_limit:

                    status = "🟡 UNDER TORQUE"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Under Torque"
                    })

                elif torque > max_limit:

                    status = "🔴 OVER TORQUE"

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Over Torque"
                    })

                else:

                    status = "🟢 OK"

                results.append([
                    f"Bolt {i + 1}",
                    present,
                    torque,
                    status
                ])

            result_df = pd.DataFrame(
                results,
                columns=[
                    "Bolt",
                    "Present",
                    "Torque",
                    "Status"
                ]
            )

            st.dataframe(
                result_df,
                use_container_width=True
            )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = wheel_end_pfmea[
                    (wheel_end_pfmea["Process"] == "Chuck Nut Assembly")
                    &
                    (wheel_end_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    severity = row["Severity"]
                    occurrence = row["Occurrence"]
                    detection = row["Detection"]

                    rpn = severity * occurrence * detection
                    log_failure(
                        module="Wheel End",
                        process="Chuk-Nut",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "Severity:",
                        severity
                    )

                    st.write(
                        "Occurrence:",
                        occurrence
                    )

                    st.write(
                        "Detection:",
                        detection
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )

if module == "Shaft Module":

    st.header("⚙️ Shaft Module")

    side = st.selectbox(
        "Select Side",
        [
            "LH Shaft",
            "RH Shaft"
        ]
    )
    process = st.selectbox(
        "Select Process",
        [
            "Sealant Application",
            "Shaft Verification",
            "Shaft Fitment",
            "Shaft Alignment",
            "Shaft Bolt Tightening"
        ]
    )
    if process == "Sealant Application":

        st.subheader(
            f"{side} - Sealant Application"
        )

        failures = []

        sealant = st.selectbox(
            "Sealant Applied?",
            ["Yes", "No"]
        )

        if st.button("Evaluate Sealant"):

            if sealant == "No":

                failures.append({
                    "location": "Sealant Application",
                    "failure": "Sealant Missing"
                })

                st.error(
                    "❌ Sealant Missing"
                )

            else:

                st.success(
                    "🟢 Sealant Applied Correctly"
                )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = shaft_pfmea[
                    (shaft_pfmea["Process"] == "Sealant Application")
                    &
                    (shaft_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    rpn = (
                            row["Severity"]
                            * row["Occurrence"]
                            * row["Detection"]
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
    elif process == "Shaft Verification":

        st.subheader(
            f"{side} - Shaft Verification"
        )

        failures = []

        installed_shaft = st.selectbox(
            "Installed Shaft",
            [
                "LH Shaft",
                "RH Shaft"
            ]
        )

        if st.button("Verify Shaft"):

            if installed_shaft != side:

                failures.append({
                    "location": "Shaft Verification",
                    "failure": "Wrong Shaft Installed"
                })

                st.error(
                    "❌ Wrong Shaft Installed"
                )

            else:

                st.success(
                    "🟢 Correct Shaft Installed"
                )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = shaft_pfmea[
                    (shaft_pfmea["Process"] == "Shaft Verification")
                    &
                    (shaft_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    rpn = (
                            row["Severity"]
                            * row["Occurrence"]
                            * row["Detection"]
                    )
                    log_failure(
                        module="Shaft",
                        process="Shaft Verification",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
    elif process == "Shaft Fitment":

        st.subheader(
            f"{side} - Shaft Fitment"
        )

        failures = []

        shaft_present = st.selectbox(
            "Shaft Present?",
            ["Yes", "No"]
        )

        if st.button("Evaluate Shaft Fitment"):

            if shaft_present == "No":

                failures.append({
                    "location": "Shaft Fitment",
                    "failure": "Shaft Missing"
                })

                st.error(
                    "❌ Shaft Missing"
                )

            else:

                st.success(
                    "🟢 Shaft Installed"
                )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = shaft_pfmea[
                    (shaft_pfmea["Process"] == "Shaft Fitment")
                    &
                    (shaft_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    rpn = (
                            row["Severity"]
                            * row["Occurrence"]
                            * row["Detection"]
                    )
                    log_failure(
                        module="Shaft",
                        process="Shaft Fitment",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
    elif process == "Shaft Alignment":

        st.subheader(
            f"{side} - Shaft Alignment"
        )

        failures = []

        alignment = st.selectbox(
            "Alignment Status",
            [
                "Aligned",
                "Misaligned"
            ]
        )

        if st.button("Evaluate Alignment"):

            if alignment == "Misaligned":

                failures.append({
                    "location": "Shaft Alignment",
                    "failure": "Misalignment"
                })

                st.error(
                    "❌ Shaft Misalignment Detected"
                )

            else:

                st.success(
                    "🟢 Shaft Properly Aligned"
                )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = shaft_pfmea[
                    (shaft_pfmea["Process"] == "Shaft Alignment")
                    &
                    (shaft_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    severity = row["Severity"]
                    occurrence = row["Occurrence"]
                    detection = row["Detection"]

                    rpn = (
                            severity *
                            occurrence *
                            detection
                    )
                    log_failure(
                        module="Shaft",
                        process="Shaft Allignment",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "Severity:",
                        severity
                    )

                    st.write(
                        "Occurrence:",
                        occurrence
                    )

                    st.write(
                        "Detection:",
                        detection
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )
    elif process == "Shaft Bolt Tightening":

        st.subheader(
            f"{side} - Shaft Bolt Tightening"
        )

        target = 180

        min_limit = 171
        max_limit = 189

        st.info(
            f"Target Torque = {target} Nm | "
            f"Min = {min_limit} Nm | "
            f"Max = {max_limit} Nm"
        )

        h1, h2, h3 = st.columns([1, 1, 1])

        with h1:
            st.markdown("### Bolt No")

        with h2:
            st.markdown("### Present")

        with h3:
            st.markdown("### Torque")

        present_list = []
        torque_list = []

        for i in range(6):
            c1, c2, c3 = st.columns([1, 1, 1])

            with c1:
                st.write(f"Bolt {i + 1}")

            with c2:
                present = st.selectbox(
                    f"Shaft Present {i}",
                    ["Yes", "No"],
                    index=0,
                    label_visibility="collapsed",
                    key=f"shaft_present_{i}"
                )

                present_list.append(present)

            with c3:
                torque = st.number_input(
                    f"Shaft Torque {i}",
                    min_value=0.0,
                    step=0.1,
                    label_visibility="collapsed",
                    key=f"shaft_torque_{i}"
                )

                torque_list.append(torque)

        if st.button("Evaluate Shaft Bolts"):

            failures = []

            results = []

            ok_count = 0
            under_count = 0
            over_count = 0
            missing_count = 0

            for i in range(6):

                present = present_list[i]
                torque = torque_list[i]

                if present == "No":

                    status = "⚫ MISSING BOLT"

                    missing_count += 1

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Missing Bolt"
                    })

                elif torque < min_limit:

                    status = "🟡 UNDER TORQUE"

                    under_count += 1

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Under Torque"
                    })

                elif torque > max_limit:

                    status = "🔴 OVER TORQUE"

                    over_count += 1

                    failures.append({
                        "location": f"Bolt {i + 1}",
                        "failure": "Over Torque"
                    })

                else:

                    status = "🟢 OK"

                    ok_count += 1

                results.append([
                    f"Bolt {i + 1}",
                    present,
                    torque,
                    status
                ])

            st.divider()

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric("Total", 6)
            c2.metric("OK", ok_count)
            c3.metric("Missing", missing_count)
            c4.metric("Under", under_count)
            c5.metric("Over", over_count)

            compliance = round(
                (ok_count / 6) * 100,
                2
            )

            st.metric(
                "Compliance %",
                compliance
            )

            result_df = pd.DataFrame(
                results,
                columns=[
                    "Bolt",
                    "Present",
                    "Torque",
                    "Status"
                ]
            )

            st.dataframe(
                result_df,
                use_container_width=True
            )

            for item in failures:

                location = item["location"]
                failure_mode = item["failure"]

                pfmea_record = shaft_pfmea[
                    (shaft_pfmea["Process"] == "Shaft Bolt Tightening")
                    &
                    (shaft_pfmea["FailureMode"] == failure_mode)
                    ]

                if not pfmea_record.empty:
                    row = pfmea_record.iloc[0]

                    severity = row["Severity"]
                    occurrence = row["Occurrence"]
                    detection = row["Detection"]

                    rpn = (
                            severity *
                            occurrence *
                            detection
                    )
                    log_failure(
                        module="Shaft",
                        process="Shaft Bolt Tightning",
                        location=item["location"],
                        failure_mode=row["FailureMode"],
                        rpn=rpn
                    )

                    st.divider()

                    st.subheader(
                        f"PFMEA Analysis - {location}"
                    )

                    st.write(
                        "Failure Mode:",
                        row["FailureMode"]
                    )

                    st.write(
                        "Failure Effect:",
                        row["FailureEffect"]
                    )

                    st.write(
                        "Failure Cause:",
                        row["FailureCause"]
                    )

                    st.write(
                        "Severity:",
                        severity
                    )

                    st.write(
                        "Occurrence:",
                        occurrence
                    )

                    st.write(
                        "Detection:",
                        detection
                    )

                    st.write(
                        "RPN:",
                        rpn
                    )

# ==================================================
# BRAKE MODULE
# ==================================================

if module == "Brake Module":

    st.header("🛑 Brake Module")

    side = st.selectbox(
        "Select Side",
        [
            "LH Brake",
            "RH Brake"
        ]
    )

    assembly = st.selectbox(
        "Select Assembly",
        [
            "Brake Caliper Assembly",
            "Brake Chamber Assembly",
            "ABS Sensor Assembly"
        ]
    )

    # ==========================================
    # BRAKE CALIPER ASSEMBLY
    # ==========================================

    if assembly == "Brake Caliper Assembly":

        process = st.selectbox(
            "Select Process",
            [
                "Caliper Verification",
                "Caliper Alignment",
                "Caliper Bolt Tightening"
            ]
        )

        # ----------------------------------
        # CALIPER VERIFICATION
        # ----------------------------------

        if process == "Caliper Verification":

            st.subheader(
                f"{side} - Caliper Verification"
            )

            failures = []

            caliper_present = st.selectbox(
                "Caliper Present?",
                ["Yes", "No"]
            )

            installed_caliper = st.selectbox(
                "Installed Caliper",
                [
                    "LH Brake",
                    "RH Brake"
                ]
            )

            if st.button("Verify Caliper"):

                if caliper_present == "No":

                    failures.append({
                        "location": "Caliper Verification",
                        "failure": "Caliper Missing"
                    })

                    st.error(
                        "❌ Caliper Missing"
                    )

                elif installed_caliper != side:

                    failures.append({
                        "location": "Caliper Verification",
                        "failure": "Wrong Caliper Installed"
                    })

                    st.error(
                        "❌ Wrong Caliper Installed"
                    )

                else:

                    st.success(
                        "🟢 Correct Caliper Installed"
                    )

                for item in failures:

                    pfmea_record = brake_pfmea[
                        (brake_pfmea["Process"] == "Brake Caliper Verification")
                        &
                        (brake_pfmea["FailureMode"] == item["failure"])
                    ]

                    if not pfmea_record.empty:

                        row = pfmea_record.iloc[0]

                        rpn = (
                            row["Severity"]
                            *
                            row["Occurrence"]
                            *
                            row["Detection"]
                        )
                        log_failure(
                            module="Brake",
                            process="Brake Caliper Verification",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(
                            f"PFMEA Analysis - {item['location']}"
                        )

                        st.write(
                            "Failure Mode:",
                            row["FailureMode"]
                        )

                        st.write(
                            "Failure Effect:",
                            row["FailureEffect"]
                        )

                        st.write(
                            "Failure Cause:",
                            row["FailureCause"]
                        )

                        st.write(
                            "RPN:",
                            rpn
                        )

        # ----------------------------------
        # CALIPER ALIGNMENT
        # ----------------------------------

        elif process == "Caliper Alignment":

            st.subheader(

                f"{side} - Caliper Alignment"

            )

            failures = []

            alignment = st.selectbox(

                "Alignment Status",

                [

                    "Aligned",

                    "Misaligned"

                ]

            )

            if st.button("Evaluate Caliper Alignment"):

                if alignment == "Misaligned":

                    failures.append({

                        "location": "Caliper Alignment",

                        "failure": "Misalignment"

                    })

                    st.error(

                        "❌ Caliper Misalignment Detected"

                    )


                else:

                    st.success(

                        "🟢 Caliper Properly Aligned"

                    )

                for item in failures:

                    pfmea_record = brake_pfmea[

                        (brake_pfmea["Process"] == "Brake Caliper Alignment")

                        &

                        (brake_pfmea["FailureMode"] == item["failure"])

                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (

                                row["Severity"]

                                *

                                row["Occurrence"]

                                *

                                row["Detection"]

                        )
                        log_failure(
                            module="Brake",
                            process="Brake Caliper Alignment",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(

                            f"PFMEA Analysis - {item['location']}"

                        )

                        st.write(

                            "Failure Mode:",

                            row["FailureMode"]

                        )

                        st.write(

                            "Failure Effect:",

                            row["FailureEffect"]

                        )

                        st.write(

                            "Failure Cause:",

                            row["FailureCause"]

                        )

                        st.write(

                            "Severity:",

                            row["Severity"]

                        )

                        st.write(

                            "Occurrence:",

                            row["Occurrence"]

                        )

                        st.write(

                            "Detection:",

                            row["Detection"]

                        )

                        st.write(

                            "RPN:",

                            rpn

                        )

        # ----------------------------------
        # CALIPER BOLT TIGHTENING
        # ----------------------------------

        elif process == "Caliper Bolt Tightening":

            st.subheader(

                f"{side} - Caliper Bolt Tightening"

            )

            target = 180

            min_limit = 171

            max_limit = 189

            st.info(

                f"Target Torque = {target} Nm | "

                f"Min = {min_limit} Nm | "

                f"Max = {max_limit} Nm"

            )

            h1, h2, h3 = st.columns([1, 1, 1])

            with h1:

                st.markdown("### Bolt No")

            with h2:

                st.markdown("### Present")

            with h3:

                st.markdown("### Torque")

            present_list = []

            torque_list = []

            for i in range(6):
                c1, c2, c3 = st.columns([1, 1, 1])

                with c1:
                    st.write(f"Bolt {i + 1}")

                with c2:
                    present = st.selectbox(

                        f"Caliper Present {i}",

                        ["Yes", "No"],

                        index=0,

                        label_visibility="collapsed",

                        key=f"cal_present_{i}"

                    )

                    present_list.append(present)

                with c3:
                    torque = st.number_input(

                        f"Caliper Torque {i}",

                        min_value=0.0,

                        step=0.1,

                        label_visibility="collapsed",

                        key=f"cal_torque_{i}"

                    )

                    torque_list.append(torque)

            if st.button("Evaluate Caliper Bolts"):

                failures = []

                results = []

                ok_count = 0

                under_count = 0

                over_count = 0

                missing_count = 0

                for i in range(6):

                    present = present_list[i]

                    torque = torque_list[i]

                    if present == "No":

                        status = "⚫ MISSING BOLT"

                        missing_count += 1

                        failures.append({

                            "location": f"Bolt {i + 1}",

                            "failure": "Missing Bolt"

                        })


                    elif torque < min_limit:

                        status = "🟡 UNDER TORQUE"

                        under_count += 1

                        failures.append({

                            "location": f"Bolt {i + 1}",

                            "failure": "Under Torque"

                        })


                    elif torque > max_limit:

                        status = "🔴 OVER TORQUE"

                        over_count += 1

                        failures.append({

                            "location": f"Bolt {i + 1}",

                            "failure": "Over Torque"

                        })


                    else:

                        status = "🟢 OK"

                        ok_count += 1

                    results.append([

                        f"Bolt {i + 1}",

                        present,

                        torque,

                        status

                    ])

                st.divider()

                c1, c2, c3, c4, c5 = st.columns(5)

                c1.metric("Total", 6)

                c2.metric("OK", ok_count)

                c3.metric("Missing", missing_count)

                c4.metric("Under", under_count)

                c5.metric("Over", over_count)

                compliance = round(

                    (ok_count / 6) * 100,

                    2

                )

                st.metric(

                    "Compliance %",

                    compliance

                )

                result_df = pd.DataFrame(

                    results,

                    columns=[

                        "Bolt",

                        "Present",

                        "Torque",

                        "Status"

                    ]

                )

                st.dataframe(

                    result_df,

                    use_container_width=True

                )

                for item in failures:

                    pfmea_record = brake_pfmea[

                        (brake_pfmea["Process"] == "Brake Caliper Bolt Tightening")

                        &

                        (brake_pfmea["FailureMode"] == item["failure"])

                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (

                                row["Severity"]

                                *

                                row["Occurrence"]

                                *

                                row["Detection"]

                        )
                        log_failure(
                            module="Brake",
                            process="Brake Caliper Bolt Tightening",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(

                            f"PFMEA Analysis - {item['location']}"

                        )

                        st.write(

                            "Failure Mode:",

                            row["FailureMode"]

                        )

                        st.write(

                            "Failure Effect:",

                            row["FailureEffect"]

                        )

                        st.write(

                            "Failure Cause:",

                            row["FailureCause"]

                        )

                        st.write(

                            "Severity:",

                            row["Severity"]

                        )

                        st.write(

                            "Occurrence:",

                            row["Occurrence"]

                        )

                        st.write(

                            "Detection:",

                            row["Detection"]

                        )

                        st.write(

                            "RPN:",

                            rpn

                        )

    # ==========================================
    # BRAKE CHAMBER ASSEMBLY
    # ==========================================

    elif assembly == "Brake Chamber Assembly":

        process = st.selectbox(
            "Select Process",
            [
                "Chamber Verification",
                "Chamber Alignment",
                "Chamber Bolt Tightening"
            ]
        )

        if process == "Chamber Verification":

            st.subheader(
                f"{side} - Chamber Verification"
            )

            failures = []

            chamber_present = st.selectbox(
                "Brake Chamber Present?",
                ["Yes", "No"]
            )

            installed_chamber = st.selectbox(
                "Installed Chamber",
                [
                    "LH Brake",
                    "RH Brake"
                ]
            )

            if st.button("Verify Chamber"):

                if chamber_present == "No":

                    failures.append({
                        "location": "Chamber Verification",
                        "failure": "Chamber Missing"
                    })

                    st.error(
                        "❌ Chamber Missing"
                    )

                elif installed_chamber != side:

                    failures.append({
                        "location": "Chamber Verification",
                        "failure": "Wrong Chamber Installed"
                    })

                    st.error(
                        "❌ Wrong Chamber Installed"
                    )

                else:

                    st.success(
                        "🟢 Correct Chamber Installed"
                    )

                for item in failures:

                    pfmea_record = brake_pfmea[
                        (brake_pfmea["Process"] == "Brake Chamber Verification")
                        &
                        (brake_pfmea["FailureMode"] == item["failure"])
                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (
                                row["Severity"]
                                *
                                row["Occurrence"]
                                *
                                row["Detection"]
                        )
                        log_failure(
                            module="Brake",
                            process="Brake Chamber Verification",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(
                            f"PFMEA Analysis - {item['location']}"
                        )

                        st.write(
                            "Failure Mode:",
                            row["FailureMode"]
                        )

                        st.write(
                            "Failure Effect:",
                            row["FailureEffect"]
                        )

                        st.write(
                            "Failure Cause:",
                            row["FailureCause"]
                        )

                        st.write(
                            "RPN:",
                            rpn
                        )


        elif process == "Chamber Alignment":

            st.subheader(

                f"{side} - Chamber Alignment"

            )

            failures = []

            alignment = st.selectbox(

                "Alignment Status",

                [

                    "Aligned",

                    "Misaligned"

                ]

            )

            if st.button("Evaluate Chamber Alignment"):

                if alignment == "Misaligned":

                    failures.append({

                        "location": "Chamber Alignment",

                        "failure": "Misalignment"

                    })

                    st.error(

                        "❌ Chamber Misalignment Detected"

                    )


                else:

                    st.success(

                        "🟢 Chamber Properly Aligned"

                    )

                for item in failures:

                    pfmea_record = brake_pfmea[

                        (brake_pfmea["Process"] == "Brake Chamber Alignment")

                        &

                        (brake_pfmea["FailureMode"] == item["failure"])

                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (

                                row["Severity"]

                                *

                                row["Occurrence"]

                                *

                                row["Detection"]

                        )
                        log_failure(
                            module="Brake",
                            process="Brake Chamber Alignment",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(

                            f"PFMEA Analysis - {item['location']}"

                        )

                        st.write(

                            "Failure Mode:",

                            row["FailureMode"]

                        )

                        st.write(

                            "Failure Effect:",

                            row["FailureEffect"]

                        )

                        st.write(

                            "Failure Cause:",

                            row["FailureCause"]

                        )

                        st.write(

                            "Severity:",

                            row["Severity"]

                        )

                        st.write(

                            "Occurrence:",

                            row["Occurrence"]

                        )

                        st.write(

                            "Detection:",

                            row["Detection"]

                        )

                        st.write(

                            "RPN:",

                            rpn

                        )


        elif process == "Chamber Bolt Tightening":

            st.subheader(

                f"{side} - Chamber Bolt Tightening"

            )

            target = 120

            min_limit = 114

            max_limit = 126

            st.info(

                f"Target Torque = {target} Nm | "

                f"Min = {min_limit} Nm | "

                f"Max = {max_limit} Nm"

            )

            present_list = []

            torque_list = []

            h1, h2, h3 = st.columns([1, 1, 1])

            with h1:

                st.markdown("### Bolt No")

            with h2:

                st.markdown("### Present")

            with h3:

                st.markdown("### Torque")

            for i in range(2):
                c1, c2, c3 = st.columns([1, 1, 1])

                with c1:
                    st.write(f"Bolt {i + 1}")

                with c2:
                    present = st.selectbox(

                        f"BC Present {i}",

                        ["Yes", "No"],

                        index=0,

                        label_visibility="collapsed",

                        key=f"bc_present_{i}"

                    )

                    present_list.append(present)

                with c3:
                    torque = st.number_input(

                        f"BC Torque {i}",

                        min_value=0.0,

                        step=0.1,

                        label_visibility="collapsed",

                        key=f"bc_torque_{i}"

                    )

                    torque_list.append(torque)

            if st.button("Evaluate Chamber Bolts"):

                failures = []

                results = []

                for i in range(2):

                    present = present_list[i]

                    torque = torque_list[i]

                    if present == "No":

                        status = "⚫ MISSING BOLT"

                        failures.append({

                            "location": f"Bolt {i + 1}",

                            "failure": "Missing Bolt"

                        })


                    elif torque < min_limit:

                        status = "🟡 UNDER TORQUE"

                        failures.append({

                            "location": f"Bolt {i + 1}",

                            "failure": "Under Torque"

                        })


                    elif torque > max_limit:

                        status = "🔴 OVER TORQUE"

                        failures.append({

                            "location": f"Bolt {i + 1}",

                            "failure": "Over Torque"

                        })


                    else:

                        status = "🟢 OK"

                    results.append([

                        f"Bolt {i + 1}",

                        present,

                        torque,

                        status

                    ])

                result_df = pd.DataFrame(

                    results,

                    columns=[

                        "Bolt",

                        "Present",

                        "Torque",

                        "Status"

                    ]

                )

                st.dataframe(

                    result_df,

                    use_container_width=True

                )

                for item in failures:

                    pfmea_record = brake_pfmea[

                        (brake_pfmea["Process"] == "Brake Chamber Bolt Tightening")

                        &

                        (brake_pfmea["FailureMode"] == item["failure"])

                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (

                                row["Severity"]

                                *

                                row["Occurrence"]

                                *

                                row["Detection"]

                        )
                        log_failure(
                            module="Brake",
                            process="Brake Chamber Bolt Tightening",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(

                            f"PFMEA Analysis - {item['location']}"

                        )

                        st.write(

                            "Failure Mode:",

                            row["FailureMode"]

                        )

                        st.write(

                            "Failure Effect:",

                            row["FailureEffect"]

                        )

                        st.write(

                            "Failure Cause:",

                            row["FailureCause"]

                        )

                        st.write(

                            "RPN:",

                            rpn

                        )


    # ==========================================
    # ABS SENSOR ASSEMBLY
    # ==========================================

    elif assembly == "ABS Sensor Assembly":

        process = st.selectbox(

            "Select Process",

            [

                "ABS Sensor Verification",

                "ABS Sensor Installation",

                "ABS Air Gap Verification"

            ]

        )

        # ====================================

        # ABS SENSOR VERIFICATION

        # ====================================

        if process == "ABS Sensor Verification":

            st.subheader(

                f"{side} - ABS Sensor Verification"

            )

            failures = []

            sensor_present = st.selectbox(

                "ABS Sensor Present?",

                ["Yes", "No"]

            )

            installed_sensor = st.selectbox(

                "Installed Sensor",

                [

                    "LH Brake",

                    "RH Brake"

                ]

            )

            if st.button("Verify ABS Sensor"):

                if sensor_present == "No":

                    failures.append({

                        "location": "ABS Sensor Verification",

                        "failure": "Sensor Missing"

                    })

                    st.error(

                        "❌ ABS Sensor Missing"

                    )


                elif installed_sensor != side:

                    failures.append({

                        "location": "ABS Sensor Verification",

                        "failure": "Wrong Sensor Installed"

                    })

                    st.error(

                        "❌ Wrong ABS Sensor Installed"

                    )


                else:

                    st.success(

                        "🟢 Correct ABS Sensor Installed"

                    )

                for item in failures:

                    pfmea_record = brake_pfmea[

                        (brake_pfmea["Process"] == "ABS Sensor Verification")

                        &

                        (brake_pfmea["FailureMode"] == item["failure"])

                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (

                                row["Severity"]

                                *

                                row["Occurrence"]

                                *

                                row["Detection"]

                        )
                        log_failure(
                            module="Brake",
                            process="ABS Sensor Verification",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(

                            f"PFMEA Analysis - {item['location']}"

                        )

                        st.write(

                            "Failure Mode:",

                            row["FailureMode"]

                        )

                        st.write(

                            "Failure Effect:",

                            row["FailureEffect"]

                        )

                        st.write(

                            "Failure Cause:",

                            row["FailureCause"]

                        )

                        st.write(

                            "RPN:",

                            rpn

                        )


        # ====================================

        # ABS SENSOR INSTALLATION

        # ====================================

        elif process == "ABS Sensor Installation":

            st.subheader(

                f"{side} - ABS Sensor Installation"

            )

            failures = []

            sensor_inserted = st.selectbox(

                "Sensor Fully Inserted?",

                [

                    "Yes",

                    "No"

                ]

            )

            if st.button("Evaluate Installation"):

                if sensor_inserted == "No":

                    failures.append({

                        "location": "ABS Sensor Installation",

                        "failure": "Sensor Not Fully Inserted"

                    })

                    st.error(

                        "❌ Sensor Not Fully Inserted"

                    )


                else:

                    st.success(

                        "🟢 Sensor Properly Installed"

                    )

                for item in failures:

                    pfmea_record = brake_pfmea[

                        (brake_pfmea["Process"] == "ABS Sensor Installation")

                        &

                        (brake_pfmea["FailureMode"] == item["failure"])

                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (

                                row["Severity"]

                                *

                                row["Occurrence"]

                                *

                                row["Detection"]

                        )
                        log_failure(
                            module="Brake",
                            process="ABS Sensor Installation",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.divider()

                        st.subheader(

                            f"PFMEA Analysis - {item['location']}"

                        )

                        st.write(

                            "Failure Mode:",

                            row["FailureMode"]

                        )

                        st.write(

                            "Failure Effect:",

                            row["FailureEffect"]

                        )

                        st.write(

                            "Failure Cause:",

                            row["FailureCause"]

                        )

                        st.write(

                            "RPN:",

                            rpn

                        )


        # ====================================

        # ABS AIR GAP

        # ====================================

        elif process == "ABS Air Gap Verification":

            st.subheader(

                f"{side} - ABS Air Gap Verification"

            )

            failures = []

            target = 0.8

            min_limit = 0.5

            max_limit = 1.1

            air_gap = st.number_input(

                "Measured Air Gap (mm)",

                min_value=0.0,

                step=0.1

            )

            st.info(

                f"Target = {target} mm | "

                f"Range = {min_limit} - {max_limit} mm"

            )

            if st.button("Evaluate Air Gap"):

                if (

                        air_gap < min_limit

                        or

                        air_gap > max_limit

                ):

                    failures.append({

                        "location": "ABS Air Gap Verification",

                        "failure": "Incorrect Air Gap"

                    })

                    st.error(

                        "❌ Incorrect Air Gap"

                    )


                else:

                    st.success(

                        "🟢 Air Gap Within Specification"

                    )

                for item in failures:

                    pfmea_record = brake_pfmea[

                        (brake_pfmea["Process"] == "ABS Air Gap Verification")

                        &

                        (brake_pfmea["FailureMode"] == item["failure"])

                        ]

                    if not pfmea_record.empty:
                        row = pfmea_record.iloc[0]

                        rpn = (

                                row["Severity"]

                                *

                                row["Occurrence"]

                                *

                                row["Detection"]

                        )

                        log_failure(
                            module="Brake",
                            process="ABS Air Gap Verification",
                            location=item["location"],
                            failure_mode=row["FailureMode"],
                            rpn=rpn
                        )

                        st.success("Failure Logged Successfully")

                        st.divider()

                        st.divider()

                        st.subheader(

                            f"PFMEA Analysis - {item['location']}"

                        )

                        st.write(

                            "Failure Mode:",

                            row["FailureMode"]

                        )

                        st.write(

                            "Failure Effect:",

                            row["FailureEffect"]

                        )

                        st.write(

                            "Failure Cause:",

                            row["FailureCause"]

                        )

                        st.write(

                            "RPN:",

                            rpn

                        )
elif module == "Master PFMEA Dashboard":
    banner = Image.open(
        "images/dashboard_banner.png"
    )

    st.image(
        banner,
        use_container_width=True
    )

    st.header("📊 Master PFMEA Dashboard")

    df = pd.read_csv(
        "data/failure_log.csv"
    )

    if len(df) == 0:

        st.warning(
            "No failure records available."
        )

    else:

        total_failures = len(df)

        max_rpn = df["RPN"].max()

        avg_rpn = round(
            df["RPN"].mean(),
            2
        )

        critical_count = len(
            df[df["RPN"] >= 100]
        )

        col1,col2,col3,col4 = st.columns(4)

        col1.metric(
            "Total Failures",
            total_failures
        )

        col2.metric(
            "Highest RPN",
            max_rpn
        )

        col3.metric(
            "Average RPN",
            avg_rpn
        )

        col4.metric(
            "Critical Risks",
            critical_count
        )

        st.divider()

        st.subheader(
            "Failure Log"
        )

        st.dataframe(
            df,
            use_container_width=True
        )