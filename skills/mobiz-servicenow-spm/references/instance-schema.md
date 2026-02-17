# Instance Schema: mobizdev.service-now.com

Generated: 2026-02-17 13:38 UTC

---

## Connectivity Test

Connection successful (HTTP 200)

---

## pm_project

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| time_card_preference | Allow time card reporting on | String | false | 40 |  |
| product | Product | Reference | false | 32 | Product Model |
| primary_target | Primary target | Reference | false | 32 | Target |
| assumptions | Assumptions | HTML | false | 8,000 |  |
| capex_estimate_to_completion | Capital estimate to completion | Currency | false | 20 |  |
| resources_from_resource_plan | Derive assignee list from resource plan | True/False | false | 40 |  |
| barriers | Barriers | HTML | false | 8,000 |  |
| project_manager | Project manager | Reference | false | 32 | User |
| forecast_cost_project_currency | Estimate at completion in project currency | FX Currency | false | 32 |  |
| npv_project_currency | Net present value in project currency | FX Currency | false | 32 |  |
| risk_of_performing | Risk of performing | HTML | false | 8,000 |  |
| u_remaining_effort | Remaining effort | Decimal | false | 15 |  |
| phase | Phase | String | false | 40 |  |
| forecast_cost | Estimate at completion | Currency | false | 20 |  |
| x_mobit_spm_enh_allocated_effort | Allocated effort | Decimal | false | 20 |  |
| u_default_agile_teams | Agile Teams | List | false | 4,000 | Group |
| primary_program | Program | Reference | false | 32 | Program |
| group_resource_assignee | Group resource assignee | List | false | 1,024 | Group |
| actual_cost_project_currency | Actual cost in project currency | FX Currency | false | 32 |  |
| discount_rate | Discount Rate % | Decimal | false | 15 |  |
| x_mobit_spm_enh_dynamics_opp_id | Oppurtunity ID | String | false | 60 |  |
| npv_value | Net present value | Currency | false | 20 |  |
| attr_based_planning | Attribute based planning | True/False | false | 40 |  |
| business_unit | Business Unit | Reference | false | 32 | Business Unit |
| capex_forecast_cost | Capital estimate at completion | Currency | false | 20 |  |
| auto_save | Auto save | True/False | false | 40 |  |
| enablers | Enablers | HTML | false | 8,000 |  |
| capex_estimate_to_completion_project_currency | Capital estimate to completion in project currency | FX Currency | false | 32 |  |
| project_type | Project type | String | false | 40 |  |
| expense_type | Expense type | String | false | 40 |  |
| investment_class | Investment Class | String | false | 40 |  |
| execution_type | Execution type | String | false | 40 |  |
| x_mobit_spm_enh_survey_status | Survey status | Choice | false | 40 |  |
| project_schedule_date_format | Project schedule date format | String | false | 40 |  |
| roi | Planned ROI % | Decimal | false | 15 |  |
| opex_cost_project_currency | Planned operating in project currency | FX Currency | false | 32 |  |
| investment_type | Investment Type | String | false | 40 |  |
| business_capabilities | Business Capabilities | List | false | 4,000 | Business Capability |
| update_actual_effort_from_time_card | Update actual effort from time card | String | false | 40 |  |
| backlog_definition | Backlog | Reference | false | 32 | Personal backlog |
| business_case | Business case | HTML | false | 4,000 |  |
| primary_portfolio | Portfolio | Reference | false | 32 | Portfolio |
| resource_assignee | Resource assignee | List | false | 1,024 | User |
| project_currency | Project currency | Reference | false | 32 | Currency |
| status_report_currency | Status report currency | String | false | 40 |  |
| x_mobit_spm_enh_actual_effort | Actual effort | Decimal | false | 20 |  |
| score_risk | Risk Score | Decimal | false | 15 |  |
| score_size | Size Score | Decimal | false | 15 |  |
| approved_end_date | Approved end date | Date/Time | false | 40 |  |
| budget_cost_project_currency | Budget cost in project currency | FX Currency | false | 32 |  |
| strategic_program | Strategic program | Reference | false | 32 | Strategic Program |
| x_mobit_spm_enh_payment_source | Payment source | Choice | false | 100 |  |
| x_mobit_spm_enh_planned_effort_sow | Planned effort (SOW)  | Decimal | false | 20 |  |
| x_mobit_spm_enh_project_type | Project type | Choice | false | 40 |  |
| x_mobit_spm_enh_purchase_order | Purchase Order | String | false | 100 |  |
| x_mobit_spm_enh_sales_order | Sales Order | String | false | 100 |  |
| risk | Risk | String | false | 40 |  |
| opex_estimate_to_completion | Operating estimate to completion | Currency | false | 20 |  |
| time_component_from_planned | Derive time component from planned dates | True/False | false | 40 |  |
| estimate_to_completion | Estimate to completion | Currency | false | 20 |  |
| goal | Goal | Reference | false | 32 | Goal |
| capex_forecast_cost_project_currency | Capital estimate at completion in project currency | FX Currency | false | 32 |  |
| x_mobit_spm_enh_survey_recipients | Survey Recipients | List | false | 4,000 | User |
| x_mobit_spm_enh_survey_sent_on | Survey Sent On | Date/Time | false | 40 |  |
| risk_of_not_performing | Risk of not performing | HTML | false | 8,000 |  |
| in_scope | In scope | HTML | false | 8,000 |  |
| schedule | Schedule | Reference | false | 32 | Schedule |
| impacted_business_units | Impacted Business Units | List | false | 4,000 | Business Unit |
| rate_model | Rate Model | Reference | false | 32 | Rate Model |
| strategic_objectives | Strategies | List | false | 4,000 | Strategic Objective |
| update_score_on_value_change | Recalculate score on project change | String | false | 40 |  |
| opex_estimate_to_completion_project_currency | Operating estimate to completion in project currency | FX Currency | false | 32 |  |
| irr_value | Internal rate of return % | Decimal | false | 15 |  |
| x_mobit_spm_enh_region | Region | Choice | false | 40 |  |
| primary_goal | Primary goal | Reference | false | 32 | Goal |
| department | Department | Reference | false | 32 | Department |
| capex_cost_project_currency | Planned capital in project currency | FX Currency | false | 32 |  |
| goals | Goals | List | false | 4,000 | Goal |
| cost_project_currency | Total planned cost in project currency | FX Currency | false | 32 |  |
| show_on_program_status_report | Show on Program Status Report | True/False | false | 40 |  |
| opex_forecast_cost | Operating estimate at completion | Currency | false | 20 |  |
| title | Title | String | false | 120 |  |
| risk_cost | Risk cost | Currency | false | 20 |  |
| out_of_scope | Out of scope | HTML | false | 8,000 |  |
| estimate_to_completion_project_currency | Estimate to completion in project currency | FX Currency | false | 32 |  |
| business_applications | Impacted Business Applications | List | false | 4,000 | Business Application |
| value | Planned return | Currency | false | 20 |  |
| actual_benefit_project_currency | Actual benefits in project currency | FX Currency | false | 32 |  |
| opex_forecast_cost_project_currency | Operating estimate at completion in project currency | FX Currency | false | 32 |  |
| demand | Demand | Reference | false | 32 | Demand |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| planned_benefit_project_currency | Planned benefit in project currency | FX Currency | false | 32 |  |
| score | Score | Decimal | false | 15 |  |
| x_mobit_spm_enh_commercial_contract_model | Commercial/Contract Model | Choice | false | 40 |  |
| planned_return_project_currency | Planned return in project currency | FX Currency | false | 32 |  |
| score_value | Value Score | Decimal | false | 15 |  |
| marked_for_delete | Marked for delete | True/False | false | 40 |  |
| u_on_hold_date | On Hold Date | Date/Time | false | 40 |  |
| approved_start_date | Approved start date | Date/Time | false | 40 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| state | 8 | On Hold |
| x_mobit_spm_enh_project_type | Presales | Presales |
| state | 1 | Open |
| x_mobit_spm_enh_payment_source | mobiz | Mobiz |
| state | -5 | Pending |
| x_mobit_spm_enh_payment_source | amm | AMM |
| x_mobit_spm_enh_risk_issue_type | other | Other |
| x_mobit_spm_enh_survey_status | postponed | Postponed |
| investment_type | artificial_intelligence | Artificial Intelligence |
| x_mobit_spm_enh_region | EU | EU |
| x_mobit_spm_enh_survey_status | pending_survey_response | Pending Survey Response |
| risk | moderate | Moderate |
| time_card_preference | project_task | Project tasks only |
| investment_class | run | Run |
| x_mobit_spm_enh_risk_issue_type | human resource | Human Resource |
| execution_type | waterfall | Waterfall |
| update_actual_effort_from_time_card | yes | Yes |
| investment_type | legal_and_regulatory | Legal and Regulatory |
| update_score_on_value_change | no | No |
| x_mobit_spm_enh_commercial_contract_model | t&m | T&M |
| phase | executing | Executing |
| state | 7 | Closed Skipped |
| x_mobit_spm_enh_survey_status | on_schedule | On Schedule |
| state | 4 | Closed Incomplete |
| x_mobit_spm_enh_commercial_contract_model | boh | BOH |
| state | 3 | Closed Complete |
| state | 2 | Work in Progress |
| x_mobit_spm_enh_survey_status | survey_overdue | Survey Overdue |
| x_mobit_spm_enh_commercial_contract_model | staff_aug | Staff Aug |
| x_mobit_spm_enh_region | LATAM | LATAM |
| x_mobit_spm_enh_region | APAC | APAC |
| x_mobit_spm_enh_risk_issue_type | schedule | Schedule |
| x_mobit_spm_enh_region | US | US |
| risk | low | Low |
| project_type | regular | Regular |
| x_mobit_spm_enh_region | MENA | MENA |
| time_card_preference | project_project_task | Project and project tasks |
| investment_class | change | Change |
| execution_type | agile | Agile |
| update_actual_effort_from_time_card | no | No |
| investment_type | revenue_generating | Revenue Generating |
| x_mobit_spm_enh_survey_status | survey_concluded | Survey Concluded |
| phase | monitoring_controlling | Monitoring/Controlling |
| expense_type | capex | Capex |
| x_mobit_spm_enh_risk_issue_type | technical | Technical |
| x_mobit_spm_enh_commercial_contract_model | ff | FF |
| x_mobit_spm_enh_commercial_contract_model | support | Support |
| status_report_currency | function_currency | Functional currency |
| x_mobit_spm_enh_survey_status | pending_survey_dispatch | Pending Survey Dispatch |
| risk | planning | Planning |
| project_type | workbench | Workbench |
| time_card_preference | no_time_card | No time reporting |
| investment_type | cost_reduction | Cost Reduction |
| execution_type | hybrid | Hybrid |
| phase | initiating | Initiating |
| investment_type | service_sustaining | Service Sustaining |
| risk | critical | Critical |
| project_schedule_date_format | date_time | Date and Time |
| x_mobit_spm_enh_project_type | Internal | Internal |
| state | -10 | Not Started |
| phase | closing | Closing |
| x_mobit_spm_enh_risk_issue_type | financial | Financial |
| x_mobit_spm_enh_risk_issue_type | quality | Quality |
| x_mobit_spm_enh_payment_source | ecif | ECIF |
| x_mobit_spm_enh_project_type | Billable | Billable |
| expense_type | opex | Opex |
| x_mobit_spm_enh_payment_source | other | Other |
| x_mobit_spm_enh_payment_source | client | Client |
| status_report_currency | project_currency | Project currency |
| time_card_preference | project | Project only |
| x_mobit_spm_enh_survey_status | not_applicable | Not Applicable |
| phase | delivering | Delivering |
| investment_type | end_user_experience | End User Experience |
| update_score_on_value_change | yes | Yes |
| phase | planning | Planning |
| investment_type | strategic_enabler | Strategic Enabler |
| risk | high | High |
| project_schedule_date_format | date | Date |

---

## pm_project_task

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| cost_project_currency | Total planned cost in project currency | FX Currency | false | 32 |  |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| start_sprint | Start Sprint | Reference | false | 32 | Sprint |
| scrum_team | Team | Reference | false | 32 | Team |
| actual_benefit_project_currency | Actual benefits in project currency | FX Currency | false | 32 |  |
| capex_cost_project_currency | Planned capital in project currency | FX Currency | false | 32 |  |
| planned_benefit_project_currency | Planned benefit in project currency | FX Currency | false | 32 |  |
| link | Link | True/False | false | 40 |  |
| opex_cost_project_currency | Planned operating in project currency | FX Currency | false | 32 |  |
| group_resource_assignee | Group resource assignee | List | false | 1,024 | Group |
| test_execution_suite | Test execution suite | Reference | false | 32 | Test execution suite |
| actual_cost_project_currency | Actual cost in project currency | FX Currency | false | 32 |  |
| x_mobit_spm_enh_external_owner | External assignee | String | false | 100 |  |
| agile_rollup_dates | Rollup dates from stories | True/False | false | 40 |  |
| project | Project | Composite Field | false | 300 |  |
| expense_type | Expense type | String | false | 40 |  |
| end_sprint | End Sprint | Reference | false | 32 | Sprint |
| project_currency | Project currency | Reference | false | 32 | Currency |
| resource_assignee | Resource assignee | List | false | 1,024 | User |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| expense_type | capex | Capex |
| expense_type | opex | Opex |

---

## pm_milestone

**Table not accessible** (may require plugin activation)

---

## pm_portfolio

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| sys_class_name | Task type | System Class Name | false | 80 |  |
| sys_created_by | Created by | String | false | 40 |  |
| state | State | String | false | 40 |  |
| sys_domain | Domain | Domain ID | false | 32 |  |
| sys_updated_on | Updated | Date/Time | false | 40 |  |
| active | Active | True/False | false | 40 |  |
| portfolio_manager | Portfolio manager | Reference | false | 32 | User |
| department | Department | Reference | false | 32 | Department |
| sys_mod_count | Updates | Integer | false | 40 |  |
| description | Description | String | false | 4,000 |  |
| sys_updated_by | Updated by | String | false | 40 |  |
| name | Name | String | false | 40 |  |
| sys_domain_path | Domain Path | Domain Path | false | 255 |  |
| business_unit | Business Unit | Reference | false | 32 | Business Unit |
| sys_created_on | Created | Date/Time | false | 40 |  |
| category | Category | String | false | 40 |  |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| state | charter | Charter |
| category | ttb | Transform business |
| category | gtb | Grow business |
| state | define | Define |
| category | rtb | Run business |
| state | analyse | Analyze |
| state | approve | Approve |

---

## pm_program

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| business_unit | Business Unit | Reference | false | 32 | Business Unit |
| scoring | Scoring | Glide Var | false | 32 | Scoring Framework Attribute |
| program_manager | Program manager | Reference | false | 32 | User |
| roi | Planned ROI % | Decimal | false | 15 |  |
| scope_status | Scope Status | String | false | 40 |  |
| impacted_business_units | Impacted Business Units | List | false | 4,000 | Business Unit |
| score_risk | Risk | Decimal | false | 15 |  |
| investment_type | Investment Type | String | false | 40 |  |
| phase | Phase | String | false | 40 |  |
| score_size | Size | Decimal | false | 15 |  |
| risk | Risk | String | false | 40 |  |
| scoring_framework | Scoring framework | Reference | false | 32 | Scoring Framework |
| strategic_objectives | Strategies | List | false | 4,000 | Strategic Objective |
| related_portfolios | Project/Demand Portfolios | List | false | 4,000 | Portfolio |
| global_rank | Global rank | Long | false | 40 |  |
| goals | Goals | List | false | 4,000 | Goal |
| portfolio | Portfolio | Reference | false | 32 | Portfolio |
| resource_status | Resource Status | String | false | 40 |  |
| cost_status | Cost Status | String | false | 40 |  |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| score | Score | Decimal | false | 15 |  |
| primary_goal | Primary goal | Reference | false | 32 | Goal |
| planned_return | Planned returns | Currency | false | 20 |  |
| department | Department | Reference | false | 32 | Department |
| score_value | Value | Decimal | false | 15 |  |
| primary_target | Primary target | Reference | false | 32 | Target |
| schedule_status | Schedule Status | String | false | 40 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| risk | high | High |
| phase | closing | Closing |
| schedule_status | red | Red |
| scope_status | red | Red |
| investment_type | legal_and_regulatory | Legal and Regulatory |
| cost_status | red | Red |
| phase | initiating | Initiating |
| risk | moderate | Moderate |
| resource_status | green | Green |
| investment_type | revenue_generating | Revenue Generating |
| phase | planning | Planning |
| risk | low | Low |
| schedule_status | green | Green |
| scope_status | green | Green |
| investment_type | cost_reduction | Cost Reduction |
| cost_status | green | Green |
| resource_status | yellow | Yellow |
| investment_type | service_sustaining | Service Sustaining |
| phase | executing | Executing |
| risk | planning | Planning |
| schedule_status | yellow | Yellow |
| scope_status | yellow | Yellow |
| investment_type | end_user_experience | End User Experience |
| cost_status | yellow | Yellow |
| resource_status | red | Red |
| investment_type | strategic_enabler | Strategic Enabler |
| risk | critical | Critical |
| phase | delivering | Delivering |

---

## rm_epic

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| theme | Theme | Reference | false | 32 | Theme |
| color | Color | Reference | false | 32 | Color Definition |
| external_identifier | External Identifier | Reference | false | 32 | External Identifiers |
| total_story_count | Total story count | Integer | false | 40 |  |
| expense_type | Expense type | String | false | 40 |  |
| product | Product | Reference | false | 32 | Product Model |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| pm_portfolio | Portfolio | Reference | false | 32 | Portfolio |
| program | Program | Reference | false | 32 | Program |
| completed_estimate | Completed estimate | Integer | false | 40 |  |
| completed_count | Completed count | Integer | false | 40 |  |
| parent_epic | Parent epic | Reference | false | 32 | Epic |
| demand | Demand | Reference | false | 32 | Demand |
| percent_complete_by_count | Percent complete by count | Percent Complete | false | 15 |  |
| percent_complete_by_estimate | Percent complete by estimate | Percent Complete | false | 15 |  |
| total_estimate | Total estimate | Integer | false | 40 |  |
| strategic_program | Strategic program | Reference | false | 32 | Strategic Program |
| global_rank | Global rank | Long | false | 40 |  |
| missing_estimates | Missing estimates | Integer | false | 40 |  |
| department | Department | Reference | false | 32 | Department |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| expense_type | capex | Capex |
| state | 2 | Work in progress |
| state | 1 | Ready |
| expense_type | opex | Opex |
| state | 4 | Cancelled |
| state | -6 | Draft |
| state | 3 | Complete |

---

## rm_story

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| blocked_reason | Blocked reason | String | false | 1,000 |  |
| eap_config | Enterprise agile configuration | Reference | false | 32 | Enterprise agile configuration |
| classification | Classification | String | false | 40 |  |
| parent_work_item | Parent work item | Reference | false | 32 | Enterprise agile planning item |
| u_application | Application | Choice | true | 40 |  |
| external_identifier | External Identifier | Reference | false | 32 | External Identifiers |
| prereq | Prerequisites | HTML | false | 8,000 |  |
| product | Product | Reference | false | 32 | Product Model |
| iteration | Enterprise agile iteration | Reference | false | 32 | Enterprise agile iteration |
| defect | Defect | Reference | false | 32 | Defect |
| release_index | Release Index | Order Index | false | 40 |  |
| release | Release | Reference | false | 32 | Scrum release |
| backlog_definition | Backlog definition | Reference | false | 32 | Personal backlog |
| blocked | Blocked | True/False | false | 40 |  |
| is_enabler | Enabler | True/False | false | 40 |  |
| theme | Theme | Reference | false | 32 | Theme |
| team_index | Team Index | Order Index | false | 40 |  |
| demand | Demand | Reference | false | 32 | Demand |
| project_index | Project Index | Order Index | false | 40 |  |
| project_phase | Project phase | Reference | true | 32 | Project Task |
| story_points | Points | Integer | false | 40 |  |
| eap_team | Team | Reference | true | 32 | Enterprise agile team |
| original_task | Original task | Reference | false | 32 | Task |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| type | Type | String | false | 40 |  |
| created_by_now_assist | Created by now assist | True/False | false | 40 |  |
| epic | Epic | Reference | false | 32 | Epic |
| acceptance_criteria | Acceptance criteria | HTML | false | 4,000 |  |
| enhancement | Enhancement | Reference | false | 32 | Enhancement |
| global_rank | Global rank | Long | false | 40 |  |
| group_rank | Group rank | Integer | false | 40 |  |
| sprint | Sprint | Reference | false | 32 | Sprint |
| product_rel_index | Product Index | Order Index | false | 40 |  |
| project | Project | Reference | false | 32 | Project |
| split_from | Split from | Reference | false | 32 | Story |
| sprint_index | Sprint Index | Order Index | false | 40 |  |
| u_update_sets | Update Sets | String | false | 4,000 |  |
| team | Team | Reference | false | 32 | Team |
| product_rank | Product rank | Integer | false | 40 |  |
| rank | Rank | Integer | false | 40 |  |
| backlog_type | Backlog Type | String | false | 40 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| state | -7 | جاهز للاختبار |
| u_application | finance_and_operations | Finance and Operations |
| u_application | power_platform | Power Platform |
| state | 3 | Complete |
| state | 4 | تم الإلغاء |
| backlog_type | project | Project |
| classification | Defect | Defect |
| priority | 2 | 2 - High |
| type | Documentation | Documentation |
| u_azure_devops_state | -6 | New |
| state | 2 | قيد التقدم |
| state | 1 | Ready |
| state | -6 | Draft |
| u_azure_devops_state | 4 | 03 Development Estimation |
| u_azure_devops_state | 5 | 04 Development Estimation Approval |
| u_azure_devops_state | 6 | 05 Development in Progress |
| u_azure_devops_state | 7 | 06 Development Testing |
| u_azure_devops_state | 8 | 07 Issue Resolution |
| u_azure_devops_state | 9 | 08 QC Deployment |
| u_azure_devops_state | 10 | 09 QC Testing |
| u_azure_devops_state | 11 | 10 Telgian Sign Off |
| u_azure_devops_state | 12 | 11 Production Deployment |
| u_azure_devops_state | 15 | Closed |
| u_azure_devops_state | 16 | Cancelled |
| state | 4 | Cancelled |
| classification | Feature | Feature |
| u_application | sales | Sales |
| state | 10 | Deploy/Launch |
| type | Spike | Spike |
| u_azure_devops_state | 1 | Active |
| u_azure_devops_state | 2 | 01 Validated |
| u_azure_devops_state | 3 | 02 Business Requirement Gathering |
| state | -6 | مسودة |
| u_azure_devops_state | 14 | Removed |
| u_azure_devops_state | 13 | Resolved |
| state | 2 | Work in progress |
| state | -8 | قيد الاختبار |
| priority | 3 | 3 - Moderate |
| u_application | ax_2012_r2 | AX 2012 R2 |
| backlog_type | oneoff | One Off |
| state | 11 | On Hold |
| state | -8 | Testing |
| priority | 4 | 4 - Low |
| state | 3 | مكتملة |
| state | 1 | جاهز |
| backlog_type | product | Product |
| state | -7 | Ready for testing |
| u_application | ado_maintenance | ADO Maintenance |
| type | Development | Development |
| u_application | field_service | Field Service |
| priority | 1 | 1 - Critical |

---

## rm_sprint

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| committed_points | Total committed points | Integer | false | 40 |  |
| team_points | Group capacity (points) | Integer | false | 40 |  |
| points | Points | Integer | false | 40 |  |
| actual_points | Completed points | Integer | false | 40 |  |
| external_identifier | External Identifier | Reference | false | 32 | External Identifiers |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| release | Release | Reference | true | 32 | Scrum release |
| release_team | Team | Reference | false | 32 | Team |
| story_points | Current scope points | Integer | false | 40 |  |
| iteration | Iteration | Reference | true | 32 | Enterprise agile iteration |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| state | 4 | Cancelled |
| state | 2 | Current |
| state | 3 | Complete |
| state | -6 | Draft |
| state | 1 | Planning |

---

## rm_defect

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| product | Product | Reference | false | 32 | Application Model |
| u_application | Application | Choice | true | 40 |  |
| reported_against | Reported against | Reference | false | 32 | Task |
| u_external_identifier | External Identifier | Reference | false | 32 | External Identifiers |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| u_azure_devops_state | 3 | 02 Business Requirement Gathering |
| u_azure_devops_state | 5 | 04 Development Estimation Approval |
| u_azure_devops_state | 1 | Active |
| u_azure_devops_state | 7 | 06 Development Testing |
| u_azure_devops_state | -6 | New |
| u_azure_devops_state | 13 | Resolved |
| u_azure_devops_state | 8 | 07 Issue Resolution |
| u_azure_devops_state | 16 | Cancelled |
| u_azure_devops_state | 11 | 10 Telgian Sign Off |
| u_application | power_platform | Power Platform |
| u_application | sales | Sales |
| u_azure_devops_state | 2 | 01 Validated |
| u_azure_devops_state | 4 | 03 Development Estimation |
| u_azure_devops_state | 6 | 05 Development in Progress |
| u_application | ax_2012_r2 | AX 2012 R2 |
| u_azure_devops_state | 9 | 08 QC Deployment |
| u_application | field_service | Field Service |
| u_application | ado_maintenance | ADO Maintenance |
| u_azure_devops_state | 10 | 09 QC Testing |
| u_azure_devops_state | 12 | 11 Production Deployment |
| u_azure_devops_state | 15 | Closed |
| u_azure_devops_state | 14 | Removed |
| u_application | finance_and_operations | Finance and Operations |

---

## rm_scrum_task

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| test_result | Test result | String | false | 40 |  |
| hours | Actual hours | Integer | false | 40 |  |
| blocked_reason | Blocked reason | String | false | 1,000 |  |
| story | Story | Reference | true | 32 | Story |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| planned_hours | Planned hours | Integer | false | 40 |  |
| remaining_hours | Remaining hours | Integer | false | 40 |  |
| blocked | Blocked | True/False | false | 40 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| type | 1 | Analysis |
| test_result | Failed | Fail |
| state | 2 | Work in progress |
| state | -6 | Draft |
| type | 2 | Coding |
| test_result | Skipped | Skipped |
| priority | 3 | 3 - Moderate |
| state | 1 | Ready |
| priority | 1 | 1 - Critical |
| state | 4 | Cancelled |
| priority | 4 | 4 - Low |
| test_result | Pass | Pass |
| type | 3 | Documentation |
| priority | 2 | 2 - High |
| type | 4 | Testing |
| state | 3 | Complete |

---

## resource_plan

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| program | Program | Reference | false | 32 | Program |
| planning_item | Planning item | Reference | false | 32 | Planning Item |
| planned_cost_demand_currency | Planned cost in demand currency | FX Currency | false | 32 |  |
| rate_model | Rate model | Reference | false | 32 | Rate Model |
| short_description | Name | String | false | 130 |  |
| role | Role | Reference | false | 32 | Resource Role |
| allocated_members_list | Confirmed / Allocated users | List | false | 1,024 | User |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| request_type | Request type | String | false | 40 |  |
| state | State | Integer | false | 40 |  |
| user_resource | User | Reference | false | 32 | User |
| allocated_hours | Confirmed / Allocated hours | Decimal | false | 15 |  |
| task | Task | Reference | false | 32 | Task |
| sys_domain | Domain | Domain ID | false | 32 |  |
| planned_cost | Planned cost | Currency | false | 20 |  |
| extension | Extension | String | false | 40 |  |
| extension_start_date | Extension start date | Date | false | 40 |  |
| sys_created_on | Created | Date/Time | false | 40 |  |
| demand_currency | Demand currency | Reference | false | 32 | Currency |
| assignment_type | Assignment type | String | false | 40 |  |
| migration | Migration | Choice | false | 40 |  |
| project_currency | Project currency | Reference | false | 32 | Currency |
| number | Number | String | false | 40 |  |
| operational_work_type | Operational work type | String | false | 40 |  |
| resource_rate | Resource rate | Currency | false | 20 |  |
| notes | Notes | Journal Input | false | 4,000 |  |
| sys_created_by | Created by | String | false | 40 |  |
| percent_capacity | % Capacity | Decimal | false | 15 |  |
| members_list | Members list | List | false | 1,024 | User |
| end_date | End date | Date | false | 40 |  |
| percent_allocated | % Plan | Percent Complete | false | 15 |  |
| planned_hours | Planned hours | Decimal | false | 15 |  |
| actual_cost | Actual cost | Currency | false | 20 |  |
| notes_list | Notes History | Journal List | false | 4,000 |  |
| sys_domain_path | Domain Path | Domain Path | false | 255 |  |
| employee_type | Employee type | String | false | 40 |  |
| top_task | Top task | Reference | false | 32 | Planned task |
| allocated_cost_project_currency | Confirmed/Allocated cost in project currency | FX Currency | false | 32 |  |
| portfolio | Portfolio | Reference | false | 32 | Portfolio |
| actual_cost_demand_currency | Actual cost in demand currency | FX Currency | false | 32 |  |
| actual_cost_project_currency | Actual cost in project currency | FX Currency | false | 32 |  |
| planned_cost_project_currency | Planned cost in project currency | FX Currency | false | 32 |  |
| assigned_cost | Assigned cost | Currency | false | 20 |  |
| extension_request_type | Extension Request Type | String | false | 40 |  |
| distribution_type | Allocation spread | String | false | 40 |  |
| sys_updated_on | Updated | Date/Time | false | 40 |  |
| man_days | Person days | Decimal | false | 15 |  |
| start_date | Start date | Date | false | 40 |  |
| actual_hours | Actual hours | Decimal | false | 15 |  |
| state_change_from_raw | State change from allocation workbench | True/False | false | 40 |  |
| allocated_cost_demand_currency | Confirmed/Allocated cost in demand currency | FX Currency | false | 32 |  |
| plan_type | Plan type | String | false | 40 |  |
| resource_type | Resource type | String | false | 40 |  |
| group_resource | Group | Reference | false | 32 | Group |
| assigned_hours | Assigned hours | Decimal | false | 15 |  |
| members_preference | Members preference | String | false | 40 |  |
| is_roll_up_from_allocations | Roll up from allocations | True/False | false | 40 |  |
| allocated_cost | Confirmed / Allocated cost | Currency | false | 20 |  |
| extension_value | Extension value | Decimal | false | 15 |  |
| planned_schedule | Planned schedule | Reference | false | 32 | Schedule |
| sys_mod_count | Updates | Integer | false | 40 |  |
| skills | Skills | List | false | 1,024 | Skill |
| distribution | Allocation type | String | false | 40 |  |
| sys_updated_by | Updated by | String | false | 40 |  |
| fte | FTE | Decimal | false | 15 |  |
| rate_override | Rate override | True/False | false | 40 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| state | 13 | Completion in progress |
| resource_type | role | Role |
| resource_type | group | Group |
| request_type | percent_capacity | % Capacity |
| members_preference | all_members | All members |
| migration | in_progress | In progress |
| request_type | hours | Hours |
| members_preference | specific_members | Specific members |
| operational_work_type | meeting | Meeting |
| distribution | plan_duration | Plan duration |
| operational_work_type | time_off | Time off |
| state | 4 | Rejected |
| extension | completed | Allocated |
| resource_type | user | User |
| plan_type | task | Task |
| members_preference | specific_members | Specific members |
| migration | completed | Completed |
| request_type | fte | FTE |
| state | 12 | Confirmation in progress |
| state | 10 | Cancel in progress |
| operational_work_type | training | Training |
| state | 1 | Planning |
| operational_work_type | appointment | Appointment |
| state | 5 | Change |
| plan_type | operational_work | Operational work |
| members_preference | any_member | Any member |
| migration | failed | Migration failed |
| request_type | man_days | Person Days |
| operational_work_type | ooo | Out of office |
| resource_type | attribute | Attribute |
| state | 2 | Requested |
| operational_work_type | call | Phone call |
| state | 6 | Work In progress |
| distribution_type | even | Even |
| operational_work_type | ktlo | KTLO |
| distribution | weekly | Weekly |
| state | 9 | Allocation in progress |
| members_preference | all_members | All members |
| state | 8 | Canceled |
| request_type | hours | Hours |
| operational_work_type | external_labor | External labor |
| state | 3 | Allocated |
| extension | requested | Requested |
| state | 11 | Confirmed |
| state | 7 | Completed |
| distribution_type | front_load | Front load |
| operational_work_type | admin | Admin |
| distribution | monthly | Monthly |

---

## resource_allocation

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| skill | Skill | Reference | false | 32 | Skill |
| resource_assignment | Resource assignment | Reference | false | 32 | Resource assignment |
| employee_type | Employee type | String | false | 40 |  |
| group_resource | Group | Reference | false | 32 | Group |
| demand_currency | Demand currency | Reference | false | 32 | Currency |
| allocated_cost_demand_currency | Confirmed/Allocated cost in demand currency | FX Currency | false | 32 |  |
| exchange_rate_project_currency | Project currency exchange rate | Floating Point Number | false | 40 |  |
| allocated_cost | Confirmed/Allocated cost | Currency | false | 20 |  |
| allocated_hours | Confirmed/Allocated hours | Decimal | false | 15 |  |
| sys_domain | Domain | Domain ID | false | 32 |  |
| sys_mod_count | Updates | Integer | false | 40 |  |
| end_date | End date | Date | true | 40 |  |
| user | Resource | Reference | false | 32 | User |
| sys_updated_by | Updated by | String | false | 40 |  |
| expense_type | Expense type | String | false | 40 |  |
| exchange_rate_demand_currency_date | Demand currency exchange rate date | Date | false | 40 |  |
| requested_cost_project_currency | Requested cost in project currency | FX Currency | false | 32 |  |
| project_currency | Project currency | Reference | false | 32 | Currency |
| start_date | Start date | Date | true | 40 |  |
| actual_cost | Actual cost | Currency | false | 20 |  |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| sys_domain_path | Domain Path | Domain Path | false | 255 |  |
| requested_hours | Requested hours | Decimal | false | 15 |  |
| distribution_type | Distribution type | String | false | 40 |  |
| sys_created_on | Created | Date/Time | false | 40 |  |
| role | Role | Reference | false | 32 | Resource Role |
| actual_cost_demand_currency | Actual cost in demand currency | FX Currency | false | 32 |  |
| planning_item | Planning item | Reference | false | 32 | Planning Item |
| exchange_rate_demand_currency | Demand currency exchange rate | Floating Point Number | false | 40 |  |
| allocated_cost_project_currency | Confirmed/Allocated cost in project currency | FX Currency | false | 32 |  |
| actual_cost_project_currency | Actual cost in project currency | FX Currency | false | 32 |  |
| exchange_rate_project_currency_date | Project currency exchange rate date | Date | false | 40 |  |
| requested_man_days | Person Days | Decimal | false | 15 |  |
| booking_type | Booking type | Integer | false | 40 |  |
| sys_created_by | Created by | String | false | 40 |  |
| task | Task | Reference | false | 32 | Task |
| requested_cost | Requested cost | Currency | false | 20 |  |
| actual_hours | Actual hours | Decimal | false | 15 |  |
| requested_cost_demand_currency | Requested cost in demand currency | FX Currency | false | 32 |  |
| assigned_hours | Assigned hours | Decimal | false | 15 |  |
| requested_fte | FTE | Decimal | false | 15 |  |
| resource_plan | Resource plan | Reference | true | 32 | Resource Plan |
| sys_updated_on | Updated | Date/Time | false | 40 |  |
| number | Number | String | false | 40 |  |
| assigned_cost | Assigned cost | Currency | false | 20 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| booking_type | 2 | Soft |
| booking_type | 1 | Hard |

---

## time_card

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| u_monday_note | Monday Note | String | false | 4,000 |  |
| x_mobit_work_log_work_summary | Work Summary  | String | false | 8,000 |  |
| friday | Friday | Decimal | false | 40 |  |
| user | User | Reference | false | 32 | User |
| monday | Monday | Decimal | false | 40 |  |
| remaining_effort | Remaining effort | Duration | false | 40 |  |
| sys_updated_by | Updated by | String | false | 40 |  |
| sys_created_on | Created | Date/Time | false | 40 |  |
| approved_on | Approved On | Date/Time | false | 40 |  |
| category | Category | String | false | 40 |  |
| comments | Comments | String | false | 4,000 |  |
| u_project_phase | Project Phase | Reference | false | 32 | Project Phases |
| u_sunday_note | Sunday Note | String | false | 4,000 |  |
| u_wednesday_note | Wednesday Note | String | false | 4,000 |  |
| u_thursday_note | Thursday Note | String | false | 4,000 |  |
| u_friday_note | Friday Note | String | false | 4,000 |  |
| u_tuesday_note | Tuesday Note | String | false | 4,000 |  |
| u_child_task | Child Task | Reference | false | 32 | Story |
| thursday | Thursday | Decimal | false | 40 |  |
| total | Total | Decimal | false | 40 |  |
| sys_domain_path | Domain Path | Domain Path | false | 255 |  |
| state | State | String | false | 40 |  |
| time_sheet | Time sheet | Reference | false | 32 | Time Sheet |
| rate_type | Rate type | Reference | false | 32 | Rate Type |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| sys_created_by | Created by | String | false | 40 |  |
| u_saturday_note | Saturday Note | String | false | 4,000 |  |
| u_project_role | Project Role | Reference | false | 32 | Project Role |
| week_starts_on | Week starts on | Date | false | 40 |  |
| wednesday | Wednesday | Decimal | false | 40 |  |
| resource_assignment | Resource assignment | Reference | false | 32 | Resource assignment |
| project_time_category | Project time category | Reference | false | 32 | Project Time Category |
| top_task | Top task | Reference | false | 32 | Planned task |
| approver_list | Approver list | List | false | 1,024 | User |
| labor_task | Task | String | false | 100 |  |
| sys_domain | Domain | Domain ID | false | 32 |  |
| sys_updated_on | Updated | Date/Time | false | 40 |  |
| u_rejected_by | Rejected by | Reference | false | 32 | User |
| saturday | Saturday | Decimal | false | 40 |  |
| task | Task | Reference | false | 32 | Task |
| sunday | Sunday | Decimal | false | 40 |  |
| tuesday | Tuesday | Decimal | false | 40 |  |
| u_work_summary | Work Summary | String | false | 8,000 |  |
| sys_mod_count | Updates | Integer | false | 40 |  |
| approved_by | Approved by | List | false | 1,024 | User |
| resource_plan | Resource plan | Reference | false | 32 | Resource Plan |
| notes | Notes | Journal | false | 4,000 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| category | task_travel | Task travel |
| category | ktlo | KTLO |
| category | task_work | العمل المتعلق بالمهمة |
| category | Unpaid Time Off | Unpaid Time Off |
| category | build_documentation | Build Documentation |
| category | project_work | المشروع/مهمة المشروع |
| category | Public Holiday | Public Holiday |
| category | internal_meeting | Internal Meeting |
| state | Processed | Processed |
| category | admin | Admin |
| category | lunch_breaks | Lunch / Breaks |
| category | customer_retention | Customer Retention |
| category | screening_resumes | Screening Resumes |
| category | appointment | موعد |
| category | training | Training |
| category | conducting_interviews | Conducting Interviews |
| category | training | Certification Training |
| state | Pending | Pending |
| category | internal_support | Internal Support |
| category | task_travel | انتقال المهمة |
| category | client_assigned_training | Client Assigned Training |
| category | admin | المسؤول |
| category | client_meeting | Client Meeting |
| category | Out Of Office | Out Of Office |
| category | corporate_functions | Corporate Functions |
| category | researching_on_a_specific_issue | Researching on a specific issue |
| category | time_off | إجازة |
| state | Recalled | Recalled |
| category | meeting | Meeting |
| category | external_labor | External labor |
| state | Submitted | Submitted |
| category | Sick Time Off | Sick Time Off |
| category | Paid Time Off | Paid Time Off |
| category | helping_techs_with_tickets | Helping Techs with tickets |
| category | training | التدريب |
| category | ooo | خارج المكتب |
| category | mobiz_communication | Mobiz(HR/Meeting/Emails) |
| category | ktlo | KTLO |
| state | Approved | Approved |
| category | project_work | Project Work |
| category | project | Project |
| category | people_management | People Management |
| category | on_site | On Site |
| category | onsite_work | Onsite Work |
| category | drive_time | Drive Time |
| category | meeting | اجتماع |
| category | bench | Bench |
| category | external_labor | عمالة خارجية |
| category | pto | Time Off (PTO, UPTO, Sick) |
| category | presales_work | Presales Work |
| category | ooo | Out of office |
| category | recruiting | Recruiting |
| category | call | مكالمة هاتفية |
| state | Rejected | Rejected |
| category | task_work | Task work |

---

## time_sheet

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| thursday | Thursday | Decimal | false | 15 |  |
| comments | Comments | String | false | 4,000 |  |
| sunday | Sunday | Decimal | false | 15 |  |
| saturday | Saturday | Decimal | false | 15 |  |
| sys_domain | Domain | Domain ID | false | 32 |  |
| sys_mod_count | Updates | Integer | false | 40 |  |
| sys_updated_by | Updated by | String | false | 40 |  |
| sys_domain_path | Domain Path | Domain Path | false | 255 |  |
| total_hours | Total Hours | Decimal | false | 15 |  |
| friday | Friday | Decimal | false | 15 |  |
| notes | Notes | Journal | false | 4,000 |  |
| sys_created_on | Created | Date/Time | false | 40 |  |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| wednesday | Wednesday | Decimal | false | 15 |  |
| state | State | String | false | 40 |  |
| week_starts_on | Week starts on | Date | true | 40 |  |
| tuesday | Tuesday | Decimal | false | 15 |  |
| week_ends_on | Week ends on | Date | false | 40 |  |
| sys_created_by | Created by | String | false | 40 |  |
| formatted_date | Formatted Date | String | false | 40 |  |
| monday | Monday | Decimal | false | 15 |  |
| user | User | Reference | false | 32 | User |
| sys_updated_on | Updated | Date/Time | false | 40 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| state | Approved | Approved |
| state | Rejected | Rejected |
| state | Pending | Pending |
| state | Processed | Processed |
| state | Submitted | Submitted |
| state | Recalled | Recalled |

---

## dmn_demand

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| demand_currency | Demand currency | Reference | false | 32 | Currency |
| npv_value | Net present value | Currency | false | 20 |  |
| operational_outlay | Operating expense | Currency | false | 20 |  |
| impacted_business_units | Impacted Business Units | List | false | 4,000 | Business Unit |
| scrum_story | Story | Reference | false | 32 | Story |
| risk_of_not_performing | Risk of not performing | HTML | false | 8,000 |  |
| start_date | Start date | Date | false | 40 |  |
| project | Project | Reference | false | 32 | Project |
| other_costs | Other costs | Currency | false | 20 |  |
| financial_benefit_demand_currency | Financial benefit in demand currency | FX Currency | false | 32 |  |
| in_scope | In scope | HTML | false | 8,000 |  |
| irr_value | Internal rate of return % | Decimal | false | 15 |  |
| strategic_program | Strategic program | Reference | false | 32 | Strategic Program |
| financial_benefit | Financial benefit | Currency | false | 20 |  |
| demand_actual_cost | Demand Actual Cost | Currency | false | 20 |  |
| resource_allocated_cost | Resource allocated cost | Currency | false | 20 |  |
| score_cost | Cost | Decimal | false | 15 |  |
| submitted_date | Submitted on | Date | false | 40 |  |
| score_value | Value | Decimal | false | 15 |  |
| model_id | Model ID | Reference | false | 32 | Product Model |
| project_currency | Project currency | Reference | false | 32 | Currency |
| assessment_required | Assessment Required | True/False | false | 40 |  |
| approved_end_date | Approved end date | Date | false | 40 |  |
| primary_target | Primary target | Reference | false | 32 | Target |
| capital_expense_demand_currency | Capital expense in demand currency | FX Currency | false | 32 |  |
| category | Category | String | true | 40 |  |
| capital_budget | Capital budget | Currency | false | 20 |  |
| change | Change | Reference | false | 32 | Change Request |
| expected_risk | Risk Level | String | false | 40 |  |
| rate_model | Rate Model | Reference | false | 32 | Rate Model |
| expected_roi | ROI % | Decimal | false | 15 |  |
| net_present_value_demand_currency | Net present value in demand currency | FX Currency | false | 32 |  |
| software_model | Software Model | Reference | false | 32 | Software Model |
| financial_return | Financial return | Currency | false | 20 |  |
| score | Score | Decimal | false | 15 |  |
| total_costs | Total planned cost | Currency | false | 20 |  |
| operating_budget_demand_currency | Operating budget in demand currency | FX Currency | false | 32 |  |
| demand_manager | Demand manager | Reference | false | 32 | User |
| resource_planned_cost | Resource planned cost | Currency | false | 20 |  |
| assumptions | Assumptions | HTML | false | 8,000 |  |
| calculation_type | Project calculation | String | false | 40 |  |
| scrum_epic | Epic | Reference | false | 32 | Epic |
| barriers | Barriers | HTML | false | 8,000 |  |
| operational_budget | Operating budget | Currency | false | 20 |  |
| financial_return_demand_currency | Financial return in demand currency | FX Currency | false | 32 |  |
| business_applications | Impacted Business Applications | List | false | 4,000 | Business Application |
| goal | Goal | Reference | false | 32 | Goal |
| risk_of_performing | Risk of performing | HTML | false | 8,000 |  |
| strategic_objectives | Strategies | List | false | 4,000 | Strategic Objective |
| collaborators | Collaborators | List | false | 4,000 | User |
| out_of_scope | Out of scope | HTML | false | 8,000 |  |
| score_risk | Risk | Decimal | false | 15 |  |
| investment_type | Investment Type | String | false | 40 |  |
| enhancement | Enhancement | Reference | false | 32 | Enhancement |
| requested_by | Due date | Date | false | 40 |  |
| related_records | Related Records | List | false | 1,024 | Task |
| goals | Goals | List | false | 4,000 | Goal |
| business_capabilities | Business Capabilities | List | false | 4,000 | Business Capability |
| demand_actual_effort | Demand Actual Effort | Duration | false | 40 |  |
| score_size | Size | Decimal | false | 15 |  |
| score_strategic_allignment | Strategic Alignment | Decimal | false | 15 |  |
| approved_start_date | Approved start date | Date | false | 40 |  |
| labor_costs | Labor costs | Currency | false | 20 |  |
| submitter | Submitted by | Reference | false | 32 | User |
| business_unit | Business Unit | Reference | false | 32 | Business Unit |
| primary_program | Program | Reference | false | 32 | Program |
| actual_cost_demand_currency | Actual cost in demand currency | FX Currency | false | 32 |  |
| product | Product | Reference | false | 32 | Product Model |
| primary_goal | Primary goal | Reference | false | 32 | Goal |
| enablers | Enablers | HTML | false | 8,000 |  |
| capital_outlay | Capital expense | Currency | false | 20 |  |
| capital_budget_demand_currency | Capital budget in demand currency | FX Currency | false | 32 |  |
| project_manager | Project Manager | Reference | false | 32 | User |
| stage | Stage | Decoration | false | 40 |  |
| close_demand | Close Demand | String | false | 40 |  |
| expense_type | Expense type | String | false | 40 |  |
| investment_class | Investment Class | String | false | 40 |  |
| size | T-Shirt size | String | false | 40 |  |
| type | Type | String | true | 40 |  |
| demand | Demand | Composite Field | false | 300 |  |
| defect | Defect | Reference | false | 32 | Defect |
| operating_expense_demand_currency | Operating expense in demand currency | FX Currency | false | 32 |  |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| idea | Idea | Reference | false | 32 | Idea |
| business_case | Business case | HTML | false | 4,000 |  |
| visited_state | Visited States | String | false | 255 |  |
| department | Department | Reference | false | 32 | Department |
| total_planned_cost_demand_currency | Total planned cost in demand currency | FX Currency | false | 32 |  |
| portfolio | Portfolio | Reference | false | 32 | Portfolio |
| discount_rate | Discount Rate % | Decimal | false | 15 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| category | operational | Operational |
| close_demand | on_closing_project | On closure of project |
| state | 10 | Deferred |
| calculation_type | NULL_OVERRIDE | -- None -- |
| expected_risk | critical | Critical |
| expected_risk | moderate | Moderate |
| state | 2 | Submitted |
| size | medium | M - Medium |
| expense_type | opex | Opex |
| type | scrum_epic | Epic |
| type | scrum_story | Story |
| type | enhancement | Enhancement |
| type | no_conversion_strategy | No Conversion |
| state | 9 | Completed |
| close_demand | NULL_OVERRIDE | -- None -- |
| state | 7 | Rejected |
| expected_risk | high | High |
| expected_risk | low | Low |
| type | change | Change |
| size | large | L - Large |
| state | 5 | Incomplete |
| type | no_conversion_operational | No Conversion |
| calculation_type | automatic | Automatic |
| expected_risk | planning | Planning |
| type | project | Project |
| state | 1 | Draft |
| state | 8 | Approved |
| size | xlarge | XL - Extra Large |
| state | -4 | Qualified |
| category | strategic | Strategic |
| type | defect | Defect |
| close_demand | on_creating_project | On creation of project |
| calculation_type | manual | Manual |
| state | 3 | Screening |
| size | xxlarge | XXL - Extra Extra Large |
| expense_type | capex | Capex |
| size | small | S - Small |

---

## cost_plan

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| cost_default_currency | Cost in functional currency | Decimal | false | 15 |  |
| portfolio | Portfolio | Reference | false | 32 | Portfolio |
| product_model | Product model | Reference | false | 32 | Product Model |
| functional_currency | Functional currency | Reference | false | 32 | Currency |
| forecast_cost_default_currency | Estimate at completion | Decimal | false | 15 |  |
| sys_updated_by | Updated by | String | false | 40 |  |
| start_fiscal_period | Start fiscal period | Reference | true | 32 | Fiscal period |
| quantity | Quantity | Integer | false | 40 |  |
| actual_cost_default_currency | Total actual cost | Decimal | false | 15 |  |
| sys_created_by | Created by | String | false | 40 |  |
| currency | Entered currency | Reference | true | 32 | Currency |
| top_task | Top task | Reference | false | 32 | Task |
| sys_mod_count | Updates | Integer | false | 40 |  |
| distribute_cost_by | Cost distribution | Choice | false | 40 |  |
| funding_entity | Source type | Reference | false | 32 | Investment Entity |
| sys_domain_path | Domain Path | Domain Path | false | 255 |  |
| demand_currency | Demand currency | Reference | false | 32 | Currency |
| cost_project_currency | Cost in project currency | Decimal | false | 15 |  |
| resource_type | Cost type | Reference | true | 32 | Cost Type Definition |
| role | Role | Reference | false | 32 | Resource Role |
| employee_type | Employee type | String | false | 40 |  |
| investment | Investment | Reference | false | 32 | Investment |
| cost_demand_currency | Cost in demand currency | Decimal | false | 15 |  |
| actual_cost_project_currency | Total actual cost in project currency  | Decimal | false | 15 |  |
| end_fiscal_period | End fiscal period | Reference | true | 32 | Fiscal period |
| task | Project/Demand | Reference | false | 32 | Task |
| system_default | miscellaneous | True/False | false | 40 |  |
| sys_created_on | Created | Date/Time | false | 40 |  |
| unit_cost | Unit cost | Decimal | false | 15 |  |
| program | Program | Reference | false | 32 | Program |
| cost_local_currency | Total planned cost | Decimal | false | 15 |  |
| sys_domain | Domain | Domain ID | false | 32 |  |
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| resource_plan | Resource plan | Reference | false | 32 | Resource Plan |
| recurring | Recurring | True/False | false | 40 |  |
| etc_cost_default_currency | Estimate to completion | Decimal | false | 15 |  |
| sys_updated_on | Updated | Date/Time | false | 40 |  |
| funding_entity_id | Source | Document ID | false | 32 |  |
| is_migrated_cost_plan | Is Migrated Cost Plan | True/False | false | 40 |  |
| funding_entity_table | Source entity table | Table Name | false | 80 |  |
| expense_type | Expense type | String | true | 40 |  |
| name | Name | String | true | 130 |  |
| is_labor_cost_plan | Is Labor Cost Plan | True/False | false | 40 |  |
| forecast_cost_project_currency | Estimate at completion in project currency | Decimal | false | 15 |  |
| project_currency | Project currency | Reference | false | 32 | Currency |
| actual_cost_demand_currency | Total actual cost in demand currency  | Decimal | false | 15 |  |
| etc_cost_project_currency | Estimate to completion in project currency | Decimal | false | 15 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| expense_type | capex | Capex |
| distribute_cost_by | total | Split equally across fiscal periods |
| expense_type | opex | Opex |
| distribute_cost_by | fiscal | Recurring per fiscal period |

---

## planned_task_rel_planned_task

### Fields

| Field | Label | Type | Mandatory | Max Length | Reference |
|-------|-------|------|-----------|-----------|-----------|
| sys_id | Sys ID | Sys ID (GUID) | false | 32 |  |
| parent_top_task | Parent top task | Reference | false | 32 | Planned task |
| sub_type | Sub Type | String | false | 40 |  |
| run_calc_brs | Run calculation brs | True/False | false | 40 |  |
| sys_domain | Domain | Domain ID | false | 32 |  |
| sys_domain_path | Domain Path | Domain Path | false | 255 |  |
| inter_task_dependency_type | Inter Task Dependency Type | String | false | 40 |  |
| process_flag | Process Flag | True/False | false | 40 |  |
| orig_sys_id | External Relation Id | Reference | false | 32 | Planned Task Relationship |
| external | External Relation | True/False | false | 40 |  |
| child_top_task | Child top task | Reference | false | 32 | Planned task |
| lag | Lag | Duration | false | 40 |  |

### Choice Values

| Field | Value | Label |
|-------|-------|-------|
| sub_type | ss | Start to Start |
| sub_type | ff | Finish to Finish |
| inter_task_dependency_type | hard | Hard |
| sub_type | sf | Start to Finish |
| inter_task_dependency_type | soft | Soft |
| sub_type | fs | Finish to Start |

---

## Key Users

| sys_id | Name | Email | Title |
|--------|------|-------|-------|
| 0006da8487f0f4103f597b9acebb35ac | Victoria Cole | victoria.cole@mhsinc.org | Clinician |
| 00114035c3c6a650a01d5673e40131d3 | Juan Luna | jluna@neighborshealth.com | Lead Radiology Technologist |
| 0011ccf9c3026a105bcb9df015013127 | Kimberly Hott | khott@neighborshealth.com | Physician |
| 002b043787d09d1050becb3e0ebb35d4 | Hamad Riaz | Hamad.Riaz@MHS.onmicrosoft.com | Mobiz Consultant |
| 004828a4c3e2e6105bcb9df015013105 | Jaclyn Arduini | jarduini@altusemergency.com | Registrar |
| 00533c31c34ea650a01d5673e40131ff | Larissa Hile | lhile@eer24.com | RN |
| 005b0c738718dd100fadcbb6dabb3584 | Rachel Ross | rross@MHS.onmicrosoft.com | Consultant |
| 0081816cc30b3e105bcb9df015013156 | Altus Fulfiller | Altus.Fulfiller@altus.com |  |
| 00951a4087f0f4103f597b9acebb35d0 | Meraki Support | noreply@meraki.com | Network Monitoring Service |
| 00a40266c32a86d0a01d5673e401317f | Elizabeth Beers | ebeers@glenhelen.com |  |
| 00bac8bf87d4dd100fadcbb6dabb358b | Stefanie Armer | stefanie.armer@turnbhs.org | Housing Specialist Center Star Act |
| 00c417c2c364f21066d9bdb4e40131a0 | Abdulrhman Beshr | Abdulrhman.beshr@TATWEER.SA |  |
| 00e2381087157010b12f4377cebb356e | Lina Hong | lina.hong@mhsinc.org | Case Manager |
| 00e3fc30c362e610a01d5673e401319f | SVC.AltusCH.Integration. MID.PROD | SVC.AltusCH.Integration.MID.PROD@altushealthsystem.com |  |
| 00eaccb387d09d1050becb3e0ebb3510 | Adriana Cruz | adriana.cruz@turnbhs.org | Administrative Assistant |
| 00f9acc8c317a610a01d5673e401313a | Karina Heath | kheath@neighborshealth.com | MD |
| 01017c35c3866a105bcb9df0150131b1 | Shayan Zia | shayan.zia@altushealthsystem.com |  |
| 01384836c31b6a50a01d5673e4013128 | Thomas Wright | twright@telgian.com | Vice President, Government Services & Special Projects |
| 013fc25e835aba10ba267000feaad393 | Veronica Toscano | veronica.toscano@turnbhs.org | Intern |
| 01437079c3866a105bcb9df015013152 | Josefina Zepeda | jzepeda@eer24.com | RN |
| 0146b9f38330fa50185f7000feaad3f3 | Ashley Luna | ashley.luna@turnbhs.org | Clinician |
| 01940e26c32a86d0a01d5673e401319c | Diana Rosas | DRosas@AllCare-med.com | Sono Techs |
| 0195d239c32c321066d9bdb4e40131ba | S NOW_TEST_DEV_20 | SNOW_TEST_DEV_20@neighborsehealth.com | SNOW DEV |
| 01ea79f383053614185f7000feaad324 | S now_test1113_04 | Snow_test1113_04@neighborshealth.com | TITLE |
| 020b44338718dd100fadcbb6dabb3532 | Nancy Jimenez | njimenez@turnbhs.org | Regional Coordinator |
| 0217948c83fd721039717000feaad3ec | Lori Phillips | lphillips@telgian.com | Billing Analyst |
| 0221883dc3026a105bcb9df0150131d0 | Megan Rios | mrios@neighborshealth.com | Administrative Assistant |
| 02427abe9373c29049d9764efaba10bf | Karina Servin | KServin1@allcare-med.com | Medical Assistant with Competency |
| 02451f4b870411100fadcbb6dabb350f | Virtual Agent | virtual.agent@example.com |  |
| 02647343c3f0fe5066d9bdb4e40131d7 | Estella Davila | edavila@altushealthsystem.com | REGISTERED NURSE |
| 026b0c7787d09d1050becb3e0ebb35ed | Martin Vondersaar | mvondersaar@turnbhs.org | Counselor SUD |
| 02783a96c33cb65066d9bdb4e4013106 | Paul English | PEnglish@neighborshealth.com | Physician |
| 02959e4087f0f4103f597b9acebb35be | Mike McConnell | MMcConnell@jmgsecurity.com |  |
| 02bc35c483da76d039717000feaad3e2 | Juan Sandoval | juan.sandoval@turnbhs.org | Clinician |
| 02c615d4833d7610ba267000feaad384 | Rebecca Moreland | rmoreland@telgian.com | Billing Analyst |
| 02d030f9c30ea650a01d5673e401317e | Tremekia Thomas | tthomas@altushealthsystem.com | Revenue Cycle Coordinator |
| 02d5de0487f0f4103f597b9acebb3593 | Service Ma Williams | service@mawilliamshomes.com |  |
| 02d77d499747f2106aaf73d11153afda | servicenowdev ball | sball@mobizinc.com | test |
| 02e0f035c3866a105bcb9df015013196 | Jodi Gentz | jgentz@altushealthsystem.com | LVN |
| 030148f9c3026a105bcb9df0150131b6 | Ronda Peeler | rpeeler@neighborshealth.com | Lead Administrative Assistant |
| 03014cf1c3c6a650a01d5673e4013129 | Ronald Ambe | rambe@neighborshealth.com | Medical Director |
| 030c0fe94770ce10ef836665d36d43a1 | Liliana Castellanos | liliana.castellanos@turnbhs.org | Case Manager |
| 03225833c36a765066d9bdb4e40131dd | Gina Goodwin | gina.goodwin@turnbhs.org | Facilities Specialist |
| 03284c32c31722505bcb9df015013191 | Altay Uzel | auzel@telgian.com | Sr. Fire Protection Consultant |
| 0348cdf3c3d8b910e78a0cbdc00131cd | Nupur Gupta | nupur.gupta@sanofi.com |  |
| 03580476c31b6a50a01d5673e40131d1 | Margarette Balajo | mbalajo@telgian.com | Vendor Accounts Specialist |
| 03640eeac3e686145bcb9df015013152 | Benjamin Calamore | BCalamore@ifeldkamp.com |  |
| 03760f1b47e4c61012702d12736d4351 | Enna Hasanbasic | enna.hasanbasic@turnbhs.org | Case Manager |
| 038bccb38718dd100fadcbb6dabb352c | Joel Flores | joel.flores@turnbhs.org | Program Supervisor/Team Lead Dart West |
| 0395f2e6c3ce52505bcb9df0150131fa | Rogelia Coronado | rcoronado@allcare-med.com | Janitorial Maintenance |
| 039ceb6f8790dd100fadcbb6dabb35b6 | Scott Wiseman | scott@mobizinc.com | Head of Sales, US |
| 03aab9d3c3f2b210a01d5673e4013142 | Minnie Taylor-Cherry | mtaylor-cherry2@telgian.com | Billing Analyst |
| 03bb88f787d09d1050becb3e0ebb3577 | Melissa Balent | melissa.balent@turnbhs.org | Sr Program Financial Analyst Corporate |
| 03cbe6f9c3cb6ed05bcb9df015013172 | Christopher Guadarrama, MD | cguadarrama@eer24.com |  |
| 03e9891e83da3a1039717000feaad317 | Natalie Correra | ncorrea@eer24.com |  |
| 03f3205bc3483210ad36b9ff050131ed | Perlita Cabrera | pcabrera@hospitalitydental.com |  |
| 03f395dd93cfba50759ab47d1dba101b | servicenowdev ok_test_13_02_3 | sok_test_13_02_1@allcare-med.com | Accounting Clerk |
| 03f45a8887b0f4103f597b9acebb3515 | Diasha Goins | diasha.goins@mhsinc.org | Case Manager |
| 04113075c3866a105bcb9df01501319b | Tracy Jones | tjones@altushealthsystem.com | Anesthesia Tech |
| 04118035c3c6a650a01d5673e4013168 | Fredrick Kersh | fkersh@neighborshealth.com | Physician |
| 04118cf9c3026a105bcb9df0150131f5 | Kevin Chiu | Kchiu@neighborshealth.com | Physician |
| 0419afbbc3b1c6105bcb9df01501317a | Maaz Akhtar | SMaazAkhtar@mobizinc.com | Azure Cloud Engineer |
| 0430d410c3af6a505bcb9df0150131b2 | Paul Kotula | pkotula@telgian.com | Field Inspector III |
| 04380072c31722505bcb9df01501317b | John Simpson | jsimpson@telgian.com | Sr. Signaling Systems Designer |
| 0446d610c329a2505bcb9df0150131c7 | Armani Coleman | Armani.coleman@turnbhs.org | Clinician |
| 0452bfa0c3b3a2505bcb9df01501312d | Gbaranen Gbaanador | ggbaanador@neighborshealth.com | MD |
| 04640aeac3e686145bcb9df01501313d | Chad Tucker | chad@glenhelen.com |  |
| 048761f51b9a34107695eb53604bcb71 | seo.roopasingh | seo.roopasingh@outlook.com |  |
| 04a41e4487b0f4103f597b9acebb3595 | Acctivate Support | support@acctivate.com |  |
| 04a41e4487b0f4103f597b9acebb35ee | Adam Beer | Abeer@mhsinc.org | Manager |
| 04a5168087f0f4103f597b9acebb3535 | Maria Quezada | mquezada@mhsinc.org | Contract Monitor / QA Sup |
| 04c378f1c34ea650a01d5673e40131e3 | Mariel Rodriguez | marielrodriguez@eer24.com | Registered Nurse |
| 04d127381bd60d10d70174c7dc4bcb3f | Irma Barrientos | irma.barrientos@mhsinc.org | Vocational Nurse |
| 04d5d60487f0f4103f597b9acebb35e6 | Samar Riaz | @example.com |  |
| 04fb17aac37762905bcb9df0150131d2 | Muhammad Saad | msaad@turnbhs.org | Mobiz Consultant |
| 0501fcf9c30ea650a01d5673e40131d8 | Kayla R. Taylor | ktaylor@altushealthsystem.com | Registered Nurse |
| 051b48338718dd100fadcbb6dabb35aa | Rachelle Kehoe | rkehoe@turnbhs.org | Sr. Compliance Specialist |
| 0532b5b29386b5101535ffed1dba10b8 | Paulina Unibe | paulina.unibe@turnbhs.org | SUD Counselor |
| 05380472c31722505bcb9df01501315e | Jeff Schaid | jschaid@telgian.com | Executive Vice President |
| 05380836c31b6a50a01d5673e40131f6 | David Krimmer | dkrimmer@telgian.com | Account Manager |
| 05384472c31722505bcb9df015013125 | Gerald Childers | jchilders@telgian.com | Member Board of Directors |
| 0548a8a4c3e2e6105bcb9df015013128 | Kristal Reyes | kreyes@altusdentalcare.com | Dental Assistant |
| 054b007787d09d1050becb3e0ebb354b | Jermaine Harnage | jharnage@turnbhs.org | Lead Counselor SUD |
| 054f3f0bdb6a7810ba13fa1439961934 | Lynn.Bayer | Lynn.Bayer@sanofi.com |  |
| 05643b0783b8b650ba267000feaad3a4 | Kelly Savella | ksavella@altushealthsystem.com | Registered Nurse |
| 05643f8f4730fa5085733525d36d43c4 | Ruth Sorenson | rsorenson@altushealthsystem.com | ADMINISTRATIVE ASSISTANT |
| 0564bb4f83bc7650185f7000feaad3b8 | Jessica Shrode Propst | jshrode@altushealthsystem.com | REGISTERED NURSE |
| 0568d1ffc3cf2610a01d5673e401318f | Chelsea Odle | codle@altushealthsystem.com |  |
| 05729b0ec324f21066d9bdb4e40131b3 | Shahad almutairi | Shahad.almutairi@TATWEER.SA |  |
| 0573f0b9c3866a105bcb9df015013101 | Veronica Paiz | vpaiz@eer24.com | Rad Tech |
| 057b40b787d09d1050becb3e0ebb3565 |  | itvacations@turnbhs.org | IT Vacation Scheduling Calendar |
| 0591c4d187f5f010b12f4377cebb35b5 | Nicholas.Furno | Nicholas.Furno@sanofi.com |  |
| 05ab40f787d09d1050becb3e0ebb35b8 | Lasata Joshi | lasata.joshi@turnbhs.org | Program Financial Analyst |
| 05b41e8487b0f4103f597b9acebb35f9 | Andreanne Bissonnette | andreanne.ob@gmail.com |  |
| 05da84ff87d4dd100fadcbb6dabb353b | Ashley Booker | ashley.booker@turnbhs.org | Employment Specialist |
| 05f31fadc31a761066d9bdb4e401319c | Junaid Hyder | admin-jhyder@hospitalitydental.onmicrosoft.com |  |
| 060bc8f387d09d1050becb3e0ebb354e | Basty Menjivar | basty.menjivar@turnbhs.org | Mental Health Clinician |
| 061035e7c3493214ad36b9ff0501310a | S NOW_TEST543 | SNOW_TEST543@altushealthsystem.com | SNOW DEV |
| 0621883dc3026a105bcb9df01501319e | Jacquelyn Trevino | jtrevino@neighborshealth.com | Registered Nurse |
| 064089ec93c05e9049d9764efaba10b8 | Tania Valdez | tania.valdez@turnbhs.org | Clinician |
| 06499f2ac3dfee105bcb9df0150131e7 | Karen Napier | knapier@eer24.com | Ultrasound |
| 0663b471c34ea650a01d5673e40131e8 | Carly Griffin | cgriffin@eer24.com | RN |
| 06643f4f83bc7650185f7000feaad346 | Kasi Hutcherson | khutcherson@altushealthsystem.com | REGISTERED NURSE |
| 06a9edc6c3c5f2d0ad36b9ff05013162 | Laura Sundquist | laura.sundquist@turnbhs.org | Clinician |
| 06e5da4487f0f4103f597b9acebb3511 | Synology Newsletter | noreply@news.synology.com |  |
| 06e5da4487f0f4103f597b9acebb356a | Talva McLay | talva@calwestcontrols.com | Owner |
| 06f0419e934635101535ffed1dba1051 | William Choi | WChoi@Cahill.com | Director of Information Technology |
| 06f365821b06b010d70174c7dc4bcb99 | Colette Liu | colette.liu@mhsinc.org | Intern |
| 07010cf1c3c6a650a01d5673e40131f7 | Kelly Wuthrich | kwuthrich@neighborshealth.com | Radiology Technologists |
| 070148f9c3026a105bcb9df015013184 | Melinna Barrera | mbarrera@neighborshealth.com | Administrative Assistant |
| 070207e6c3f6f610a01d5673e4013106 | servicenowqa nbkb | snbkb@allcare-med.com | Accounting Clerk |
| 0715d20c87b0f4103f597b9acebb3584 | Gisela Marquez | gmarquez@hospitalitydental.com |  |
| 07284c32c31722505bcb9df01501315f | Jennifer Johnson | jjohnson@telgian.com | Account Specialist |
| 0728c036c31b6a50a01d5673e4013185 | Luis Herrera | lherrera@telgian.com | Fire Suppression Designer |
| 073f7c70c39fea10a01d5673e4013197 | Jazmin Lozano | jazmin.lozano@turnbhs.org | Administrative Assistant North Inland MHC |
| 0758c0b2c31722505bcb9df0150131ea | Janet Ballard | jballard@telgian.com | Sr. VP of Finance/Controller |
| 075b00b38718dd100fadcbb6dabb35fc | Julia Belford-Saldana | Julia.Belford-Saldana@turnbhs.org | Program Manager |
| 075f480583a5a61068537cdfeeaad3ca | Faisal Din | fdin@altushealthsystem.com | Senior Director of Facilities |
| 0772dacf87905d100fadcbb6dabb3510 | QA.MHS Leadership | QA.MHS.Leadership@mobizinc.com | QA User - Leadership |
| 078c6363879c5d1050becb3e0ebb353d | David Wang | dwang@mobizinc.com | DevOps Engineer |
| 07933cb1c34ea650a01d5673e40131ac | FRONT Desk email BEAUMONT | fd.beaumont@eer24.com |  |
| 0796e0bb938c1a1049d9764efaba1008 | Ahmed Z. Eldabe Eldabe | aeldabe@stc.com.sa |  |
| 079c2b63879c5d1050becb3e0ebb35d1 | MBZConferenceRoom  | mbz.red-conference@mobizinc.com |  |
| 07a40666c32a86d0a01d5673e40131f7 | Teodora Garcia | TGarcia@allcare-med.com | Nurse Practitioner |
| 07ab7d7387b1f410b12f4377cebb3574 | Cheri Morgan | cheri.morgan@mhsinc.org | Case Manager Clinical |
| 07ba80b387d09d1050becb3e0ebb356e | Peter Flores | pflores@turnbhs.org | SUD Counselor |
| 07be9345c35c3d90e78a0cbdc001319b | Christine Larsen | christine.larsen@bsbna.com | Sr IT Project Manager |
| 07f45a8887b0f4103f597b9acebb352b | Diego Villavicencio | diego.villavicencio@mhsinc.org | Financial Analyst |
| 07f62d1fc333a6905bcb9df015013114 | Muhammad ArbabTariq | atariq@mobizinc.com | Unified Communications Engineer |
| 08118035c3c6a650a01d5673e4013136 | Maria Ibarra | mibarra@neighborshealth.com | ER Technician |
| 08118cf9c3026a105bcb9df0150131c3 | Eric Roberson | eroberson@neighborshealth.com | Physician |
| 081cacc7c3fbe2905bcb9df015013137 | Hung Do | hdo@neighborshealth.com | Emergency Center Registered Nurse |
| 08388436c31b6a50a01d5673e401316f | David Gaskill | dgaskill@telgian.com | Senior Vice President, Sales |
| 083d3f3b4745f69085733525d36d43b0 | S NOW_TESTUAT6521 | SNOW_TESTUAT6521@altushealthsystem.com | SNOW DEV |
| 08921f82c31a62905bcb9df015013197 | AAAHC Service | AAAHC@allcare-med.com |  |
| 0893bcb9c3866a105bcb9df015013178 | Megan Haas | mhaas@eer24.com | Registration |
| 08a5168087f0f4103f597b9acebb354b | MRC Email Security | mrcemailsecurity@mrcentertainment.com |  |
| 08a7d1c88319321439717000feaad3d7 | S NOW_test5412 | SNOW_test5412@neighborshealth.com | SNOWDEEV |
| 08b9b1c61b153410d70174c7dc4bcb02 | Emily Morgan | emily.morgan@mhsinc.org | Employment Specialist |
| 08cb155383e03210185f7000feaad3e8 | Taylor Beauchamp | taylor.beauchamp@turnbhs.org | Administrative Assistant |
| 08f27987c3c71a905bcb9df015013143 | Marai H.  Arjan  | marai.arjan@tarshid.com.sa | IT Director |
| 08f5128487f0f4103f597b9acebb3595 | Tiffany Reece | treece@mhsinc.org | Licensed Vocational Nurse |
| 0901303dc30ea650a01d5673e401316d | Adelyn K. Millican | amillican@altushealthsystem.com | Administrative Assistant |
| 091b003787d09d1050becb3e0ebb358d | Susan Murdock | smurdock@turnbhs.org | Program Manager |
| 09309a5283d27a10185f7000feaad352 | Tiffany LaMar | tiffany.lamar@turnbhs.org | Intern |
| 09384836c31b6a50a01d5673e401318b | John Pahr | jpahr@telgian.com | Vendor Procurement Manager |
| 094b007787d09d1050becb3e0ebb3519 | Rita Moufarrege | rita.moufarrege@turnbhs.org | Clinical Supervisor |
| 095406eac3e686145bcb9df015013128 | Extern Temecula | externtem@allcare-med.com |  |
| 096ddd2993c4d2d049d9764efaba1074 | Basim  Almutairi | BM@qm.edu.sa |  |
| 0973f0b9c3866a105bcb9df015013196 | Haylee Cave | hcave@eer24.com | RN |
| 097b40b787d09d1050becb3e0ebb35fa | Sarah Gilliland | sgilliland@turnbhs.org | Office Manager |
| 0985124087f0f4103f597b9acebb356a | Amanda Mastrup | marie.mastrup@mhsinc.org | Program Manager |
| 098de64f87145d100fadcbb6dabb3561 | SVC.Mobiz Integration.AAD | SVC.Mobiz.Integration.AAD.DEV@mobizinc.com | SVC User - Integration |
| 0995da4087f0f4103f597b9acebb35b6 | Michael Olivas | michael.olivas@mhsinc.org | Compliance Specialist |
| 099e480583a5a61068537cdfeeaad346 | Darleen E. Callahan | dcallahan@altushealthsystem.com | VP Revenue Cycle |
| 09a5968087f0f4103f597b9acebb35c8 | Nandan Dave | ndave@manh.com |  |
| 09a69ffec3dfaa50a01d5673e4013144 | Dulce Reyes | dreyes@allcare-med.com | Care Coordinator |
| 09a8c137c3d8b910e78a0cbdc00131af | Ravinder Tyagi | ravinder.tyagi@sanofi.com |  |
| 09aac4bf87d4dd100fadcbb6dabb3544 | Marzena Sudak | msudak@turnbhs.org | Administrative Assistant North Star ACT |
| 09abc4f38718dd100fadcbb6dabb3555 | Elexis Aguilar | elexis.aguilar@turnbhs.org | Case Manager |
| 09acea7cc3376910e78a0cbdc00131a0 | Alisha Doerrer | alisha.doerrer@turnbhs.org | Office Manager |
| 09ceb6eec3cad610a01d5673e401319f | Moises Leon | mleon@allcare-med.com | Janitorial Maintenance |
| 09d8ec14476eb65085733525d36d43fe | Amanda Parrette | Amanda@altushealthsystem.com | Chief People Officer |
| 09da88b387d09d1050becb3e0ebb35c9 | Raymond Ritch | raymond.ritch@turnbhs.org | SUD Counselor |
| 09ee58a4876125500fadcbb6dabb35bd | Araceli Banuelos | araceli.banuelos@turnbhs.org | Office Manager - School Based |
| 09f0e40e476d7e1085733525d36d4358 | snow now_test0212_001 | snow_test0212_001@altushealthsystem.com | test |
| 0a0516c887b0f4103f597b9acebb359f | Elizabeth Beers | EBeers@AllCare-med.com |  |
| 0a2c3cdd1b1770107695eb53604bcb12 | Michael.Stager | Michael.Stager@sanofi.com |  |
| 0a35d64c87b0f4103f597b9acebb3563 | Jazmin Astilleros | JazminA@dcgfulfillment.com |  |
| 0a3b44738718dd100fadcbb6dabb35e8 | Ana Popoca-Logue | ana.popoca@turnbhs.org | Consultant |
| 0a4810a8c3407950e78a0cbdc001310d | Michael Behnke | michael.behnke@turnbhs.org | Vice President of Human Resources |
| 0a57e7f8c36f2a90a01d5673e40131e8 | Caeli Matanky | cmatanky@allcare-med.com | Nurse Practitioner |
| 0a655ecc87b0f4103f597b9acebb3529 | Lary Chambers | Lchambers@mvcschool.org |  |
| 0a8204198306b2d0ba267000feaad303 | snow now_test251225_001 | snow_test251225_001@altushealthsystem.com | test |
| 0aa16db08771b010b12f4377cebb353f | ysakakibara | ysakakibara@crescendocollective.com |  |
| 0aaffaaeff002210b093fffffffffff0 | External Bot |  |  |
| 0abd7b6dc386a650a01d5673e4013145 | test9  | test9@austiner.onmicrosoft.com |  |
| 0ac41ec487b0f4103f597b9acebb3575 | Blythe Harris | Blythe@elegwear.com | Production Director |
| 0aced969c3f4be1066d9bdb4e4013175 | Keith Shackelford | keith.shackelford@turnbhs.org | Night Monitor |
| 0adf25d6939c9a1049d9764efaba104b | Ashley Ramos | Ashley.ramos@turnbhs.org | Consultant |
| 0aea4279836ab610ba267000feaad3d0 | Jacob Franklin | JFranklin@austiner.com | MD |
| 0b010cf1c3c6a650a01d5673e40131c5 | Karli Ayers | kayers@neighborshealth.com | Registered Nurse |
| 0b0148f9c3026a105bcb9df015013152 | Jesse De La Torre | jdelatorre@neighborshealth.com | Radiology Technologist |
| 0b014cf1c3c6a650a01d5673e401318c | Francis Gaude | fgaude@neighborshealth.com | Registered Nurse |
| 0b24cb1283d1b254ba267000feaad398 | Steven Thompson | sthompson1@altushealthsystem.com |  |
| 0b284c32c31722505bcb9df01501312d | Bree Crownover | bcrownover@telgian.com | Accounting Manager |
| 0b2e63a7c35612105bcb9df015013104 | Ubaid Rehman | URehman@mobizinc.com | Microsoft 365 Administrator |
| 0b404a144759ba9085733525d36d4312 | Olivia Flores | olivia.flores@turnbhs.org | PROGRAM SUPERVISOR |
| 0b53f879c3866a105bcb9df015013109 | David Thetford | dthetford@eer24.com | Family Medicine |
| 0b6099bb83953a10185f7000feaad3c2 | Marcie Evert | MEvert@altushealthsystem.com | Registered Nurse |
| 0b640eeac3e686145bcb9df0150131b5 | Angelica Ocampo | aocampo@allcare-med.com | LVN |
| 0b65decc87b0f4103f597b9acebb358f | Lavon Watkins | lavon@mawilliamshomes.com |  |
| 0b72dacf87905d100fadcbb6dabb350d | QA.MHS Fulfiller | QA.MHS.Fulfiller@mobizinc.com | QA User - Fulfiller |
| 0b8a00bf87d4dd100fadcbb6dabb3545 | Melissa Deer | melissa.deer@turnbhs.org | Consultant |
| 0b93b0f9c3866a105bcb9df01501315b | Marilyn Clark | mclark@eer24.com | Rad Tech |
| 0ba4c66ec3e686145bcb9df0150131ea | Angie Melgar | amelgar@allcare-med.com | Care Coordinator |
| 0bc07cb9c30ea650a01d5673e40131c5 | Brittany Humble | bhumble@altushealthsystem.com | NP Hospitalist |
| 0bd33435c34ea650a01d5673e4013193 | Andrew Hoyland | ahoyland@eer24.com | Registered Nurse |
| 0beec28c931c9a1049d9764efaba10fc | Matt Roffers | mroffers@altushealthsystem.com | Controller |
| 0bf06a86c339da10a01d5673e40131fb | Melissa Gonzales | mgonzales@hospitalitydental.com | Hygienist |

---

*End of schema introspection*
