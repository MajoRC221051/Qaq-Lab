        with ignition_column:
            ignition = st.selectbox(
                "Explicit ignition",
                [
                    "Any",
                    *sorted(tests["ignited_explicit"].dropna().unique()),
                ],
                key="explorer_ignition",
            )

        with outcome_column:
            outcome = st.selectbox(
                "Documented outcome",
                [
                    "Any",
                    *sorted(tests["observed_outcome"].dropna().unique()),
                ],
                key="explorer_outcome",
            )

        if st.button("Find supporting evidence", key="submit_flame_query"):
            query: dict[str, object] = {}
            if use_oxygen:
                query["oxygen_vol_pct"] = float(oxygen_value)
            if use_initial_airflow:
                query["airflow_start_cm_s"] = float(initial_airflow_value)
            if use_final_airflow:
                query["airflow_end_cm_s"] = float(final_airflow_value)
            if airflow_profile != "Any":
                query["airflow_profile"] = airflow_profile
            if selected_width != "Any":
                query["sample_width_cm"] = float(
                    selected_width.replace(" cm", "")
                )
            if sample_condition != "Any":
                query["reused_sample"] = (
                    "Yes" if sample_condition == "Reused sample" else "No"
                )
            if ignition != "Any":
                query["ignited_explicit"] = ignition
            if outcome != "Any":
                query["observed_outcome"] = outcome

            if query:
                st.session_state["explorer_request"] = {
                    "need": "flame",
                    "query": query,
                }
            else:
                st.warning("Select at least one condition before searching.")

        submitted = st.session_state.get("explorer_request", {})
        if submitted.get("need") == "flame":
            render_flame_results(tests, submitted["query"])

    else:
        st.markdown(
            """
            <div class="em"><div class="fixed-condition">
              <strong>Current prototype coverage:</strong> SAME is connected at investigation and report level. Condition-level SAME records have not been curated.
            </div></div>
            """,
            unsafe_allow_html=True,
        )

        focus_column, material_column = st.columns(2)
        with focus_column:
            smoke_focus = st.selectbox(
                "Research focus",
                [
                    "Smoke particle size",
                    "Smoke transport and aging",
                    "Smoke detector response",
                ],
                key="explorer_smoke_focus",
            )

        with material_column:
            smoke_material = st.selectbox(
                "Material of interest",
                [
                    "Any documented material",
                    "Teflon",
                    "Kapton",
                    "Cellulose",
                    "Silicone rubber",
                    "Dibutyl phthalate",
                    "Pyrell (SAME-R)",
                ],
                key="explorer_smoke_material",
            )

        if st.button("Find supporting evidence", key="submit_smoke_query"):
            st.session_state["explorer_request"] = {
                "need": "smoke",
                "focus": smoke_focus,
                "material": smoke_material,
            }

        submitted = st.session_state.get("explorer_request", {})
        if submitted.get("need") == "smoke":
            render_same_results(submitted)

    st.markdown(
        '<div class="footer">Ember — Evidence routing without unsupported prediction.</div>',
        unsafe_allow_html=True,
    )


st.markdown(CSS, unsafe_allow_html=True)

page = get_query_value("page", "home")
if page == "library":
    render_library()
elif page == "explorer":
    render_experiment_explorer()
else:
    render_home()
