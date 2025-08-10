import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import time

# Configure the page
st.set_page_config(
    page_title="BPM System Demo",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processes' not in st.session_state:
    st.session_state.processes = []
if 'users' not in st.session_state:
    st.session_state.users = {
        'john_doe': {'name': 'John Doe', 'role': 'Business User', 'department': 'Marketing'},
        'sarah_pmo': {'name': 'Sarah Johnson', 'role': 'PMO', 'department': 'PMO'},
        'mike_tech': {'name': 'Mike Chen', 'role': 'Technical Lead', 'department': 'IT'},
        'lisa_manager': {'name': 'Lisa Smith', 'role': 'Manager', 'department': 'IT'}
    }
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'john_doe'

# Sample data initialization
if not st.session_state.processes:
    sample_processes = [
        {
            'id': str(uuid.uuid4()),
            'title': 'Customer Portal Enhancement',
            'type': 'IT Project Request',
            'submitter': 'john_doe',
            'created_date': datetime.now() - timedelta(days=5),
            'current_step': 'Technical Team Review',
            'assigned_to': 'mike_tech',
            'status': 'In Progress',
            'sla_due': datetime.now() + timedelta(days=2),
            'steps_completed': ['Business User Submission', 'PMO Review'],
            'business_requirements': 'Enhance customer portal with new dashboard features',
            'timeline': '3 months',
            'budget': '$50,000',
            'priority': 'High'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Data Analytics Platform',
            'type': 'IT Project Request',
            'submitter': 'john_doe',
            'created_date': datetime.now() - timedelta(days=12),
            'current_step': 'Final Approval',
            'assigned_to': 'lisa_manager',
            'status': 'Pending Approval',
            'sla_due': datetime.now() + timedelta(days=1),
            'steps_completed': ['Business User Submission', 'PMO Review', 'Technical Team Review', 'PMO Validation'],
            'business_requirements': 'Implement comprehensive data analytics platform',
            'timeline': '6 months',
            'budget': '$120,000',
            'priority': 'Medium'
        }
    ]
    st.session_state.processes.extend(sample_processes)

# Helper functions
def get_sla_status(due_date):
    now = datetime.now()
    if due_date < now:
        return "Overdue", "🔴"
    elif due_date < now + timedelta(days=1):
        return "Critical", "🟡"
    else:
        return "On Track", "🟢"

def get_process_steps():
    return [
        "Business User Submission",
        "PMO Review", 
        "Technical Team Review",
        "PMO Validation",
        "Final Approval"
    ]

def create_new_process(title, business_req, timeline, budget, priority):
    process_id = str(uuid.uuid4())
    new_process = {
        'id': process_id,
        'title': title,
        'type': 'IT Project Request',
        'submitter': st.session_state.current_user,
        'created_date': datetime.now(),
        'current_step': 'PMO Review',
        'assigned_to': 'sarah_pmo',
        'status': 'In Progress',
        'sla_due': datetime.now() + timedelta(days=3),
        'steps_completed': ['Business User Submission'],
        'business_requirements': business_req,
        'timeline': timeline,
        'budget': budget,
        'priority': priority
    }
    st.session_state.processes.append(new_process)
    return process_id

# Sidebar navigation
st.sidebar.title("🔄 BPM System Demo")

# User selection
st.sidebar.subheader("Current User")
user_options = {k: f"{v['name']} ({v['role']})" for k, v in st.session_state.users.items()}
selected_user = st.sidebar.selectbox("Select User", options=list(user_options.keys()), 
                                    format_func=lambda x: user_options[x])
st.session_state.current_user = selected_user

# Navigation
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Select Page", [
    "📝 Work Management System",
    "👥 Manager's View", 
    "📊 Management Dashboard",
    "➕ New Process Request",
    "🔧 Process Templates",
    "👤 User Management",
    "📈 Advanced Analytics",
    "🔗 System Integrations",
    "⚙️ SLA Configuration"
])

# Main content area
current_user_info = st.session_state.users[st.session_state.current_user]
st.title(f"Welcome, {current_user_info['name']}")
st.caption(f"Role: {current_user_info['role']} | Department: {current_user_info['department']}")

if page == "📝 Work Management System":
    st.header("Work Management System")
    
    # Filter processes for current user
    user_processes = []
    for process in st.session_state.processes:
        if (process['assigned_to'] == st.session_state.current_user or 
            process['submitter'] == st.session_state.current_user):
            user_processes.append(process)
    
    if not user_processes:
        st.info("No tasks assigned to you currently.")
    else:
        for process in user_processes:
            with st.expander(f"🎯 {process['title']} - {process['status']}", expanded=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Current Step:** {process['current_step']}")
                    st.write(f"**Business Requirements:** {process['business_requirements']}")
                    st.write(f"**Timeline:** {process['timeline']}")
                    st.write(f"**Budget:** {process['budget']}")
                
                with col2:
                    sla_status, sla_icon = get_sla_status(process['sla_due'])
                    st.write(f"**SLA Status:** {sla_icon} {sla_status}")
                    st.write(f"**Due:** {process['sla_due'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Priority:** {process['priority']}")
                
                with col3:
                    st.write("**Progress:**")
                    steps = get_process_steps()
                    for i, step in enumerate(steps):
                        if step in process['steps_completed']:
                            st.write(f"✅ {step}")
                        elif step == process['current_step']:
                            st.write(f"🔄 {step}")
                        else:
                            st.write(f"⏳ {step}")
                
                # Action buttons based on current step and user role
                if process['assigned_to'] == st.session_state.current_user:
                    st.subheader("Actions Required")
                    
                    if process['current_step'] == 'PMO Review' and current_user_info['role'] == 'PMO':
                        st.write("**PMO Review Checklist:**")
                        req_collected = st.checkbox("✓ Business Requirements Collection", key=f"req_{process['id']}")
                        func_req = st.checkbox("✓ Functional and Non-Functional Requirements", key=f"func_{process['id']}")
                        stakeholders = st.checkbox("✓ Stakeholder Identification", key=f"stake_{process['id']}")
                        timeline_check = st.checkbox("✓ Timeline and Budget Estimates", key=f"time_{process['id']}")
                        risks = st.checkbox("✓ Risks and Constraints", key=f"risk_{process['id']}")
                        
                        if st.button(f"Complete PMO Review", key=f"complete_pmo_{process['id']}"):
                            if all([req_collected, func_req, stakeholders, timeline_check, risks]):
                                process['current_step'] = 'Technical Team Review'
                                process['assigned_to'] = 'mike_tech'
                                process['steps_completed'].append('PMO Review')
                                process['sla_due'] = datetime.now() + timedelta(days=5)
                                st.success("PMO Review completed! Task moved to Technical Team.")
                                st.rerun()
                            else:
                                st.error("Please complete all checklist items before proceeding.")
                    
                    elif process['current_step'] == 'Technical Team Review' and current_user_info['role'] == 'Technical Lead':
                        st.write("**Technical Review:**")
                        feasibility = st.selectbox("Project Feasibility", 
                                                 ["Select", "Feasible", "Needs Modification", "Not Feasible"],
                                                 key=f"feas_{process['id']}")
                        effort = st.text_input("Estimated Effort (hours)", key=f"effort_{process['id']}")
                        
                        if st.button(f"Complete Technical Review", key=f"complete_tech_{process['id']}"):
                            if feasibility != "Select" and effort:
                                process['current_step'] = 'PMO Validation'
                                process['assigned_to'] = 'sarah_pmo'
                                process['steps_completed'].append('Technical Team Review')
                                process['sla_due'] = datetime.now() + timedelta(days=2)
                                st.success("Technical Review completed! Task moved back to PMO for validation.")
                                st.rerun()
                            else:
                                st.error("Please complete all required fields.")
                    
                    elif process['current_step'] == 'PMO Validation' and current_user_info['role'] == 'PMO':
                        st.write("**PMO Validation:**")
                        alignment = st.selectbox("Business-Technical Alignment", 
                                                ["Select", "Aligned", "Minor Adjustments Needed", "Major Revisions Required"],
                                                key=f"align_{process['id']}")
                        
                        if st.button(f"Complete PMO Validation", key=f"complete_val_{process['id']}"):
                            if alignment != "Select":
                                process['current_step'] = 'Final Approval'
                                process['assigned_to'] = 'lisa_manager'
                                process['steps_completed'].append('PMO Validation')
                                process['sla_due'] = datetime.now() + timedelta(days=3)
                                st.success("PMO Validation completed! Task moved to Final Approval.")
                                st.rerun()
                            else:
                                st.error("Please select alignment status.")
                    
                    elif process['current_step'] == 'Final Approval' and current_user_info['role'] == 'Manager':
                        st.write("**Final Approval:**")
                        decision = st.selectbox("Approval Decision", 
                                               ["Select", "Approved", "Approved with Conditions", "Rejected"],
                                               key=f"decision_{process['id']}")
                        
                        if st.button(f"Make Final Decision", key=f"complete_final_{process['id']}"):
                            if decision != "Select":
                                process['steps_completed'].append('Final Approval')
                                process['status'] = 'Completed' if decision == 'Approved' else 'Rejected'
                                process['current_step'] = 'Completed'
                                st.success(f"Process {decision.lower()}!")
                                st.rerun()
                            else:
                                st.error("Please make a decision.")

elif page == "👥 Manager's View":
    st.header("Manager's View")
    
    if current_user_info['role'] not in ['Manager', 'PMO']:
        st.warning("This view is restricted to Managers and PMO users.")
    else:
        # Team workload overview
        st.subheader("Team Workload Overview")
        
        # Create workload summary
        workload_data = []
        for user_id, user_info in st.session_state.users.items():
            assigned_count = len([p for p in st.session_state.processes if p['assigned_to'] == user_id])
            overdue_count = len([p for p in st.session_state.processes 
                               if p['assigned_to'] == user_id and p['sla_due'] < datetime.now()])
            workload_data.append({
                'Employee': user_info['name'],
                'Role': user_info['role'],
                'Department': user_info['department'],
                'Assigned Tasks': assigned_count,
                'Overdue Tasks': overdue_count
            })
        
        workload_df = pd.DataFrame(workload_data)
        st.dataframe(workload_df, use_container_width=True)
        
        # SLA Compliance Overview
        st.subheader("SLA Compliance Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # SLA status pie chart
            sla_counts = {'On Track': 0, 'Critical': 0, 'Overdue': 0}
            for process in st.session_state.processes:
                if process['status'] not in ['Completed', 'Rejected']:
                    status, _ = get_sla_status(process['sla_due'])
                    sla_counts[status] += 1
            
            fig_pie = px.pie(values=list(sla_counts.values()), 
                           names=list(sla_counts.keys()),
                           title="SLA Status Distribution",
                           color_discrete_map={'On Track': 'green', 'Critical': 'yellow', 'Overdue': 'red'})
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Process status bar chart
            status_counts = {}
            for process in st.session_state.processes:
                status = process['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig_bar = px.bar(x=list(status_counts.keys()), 
                           y=list(status_counts.values()),
                           title="Process Status Overview",
                           labels={'x': 'Status', 'y': 'Count'})
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed process list
        st.subheader("All Active Processes")
        
        process_data = []
        for process in st.session_state.processes:
            if process['status'] not in ['Completed', 'Rejected']:
                assigned_user = st.session_state.users.get(process['assigned_to'], {}).get('name', 'Unknown')
                sla_status, sla_icon = get_sla_status(process['sla_due'])
                
                process_data.append({
                    'Title': process['title'],
                    'Current Step': process['current_step'],
                    'Assigned To': assigned_user,
                    'Priority': process['priority'],
                    'SLA Status': f"{sla_icon} {sla_status}",
                    'Due Date': process['sla_due'].strftime('%Y-%m-%d'),
                    'Days Since Created': (datetime.now() - process['created_date']).days
                })
        
        if process_data:
            process_df = pd.DataFrame(process_data)
            st.dataframe(process_df, use_container_width=True)
        else:
            st.info("No active processes found.")

elif page == "📊 Management Dashboard":
    st.header("Management Dashboard")
    
    # Key metrics
    st.subheader("Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_processes = len(st.session_state.processes)
    active_processes = len([p for p in st.session_state.processes if p['status'] not in ['Completed', 'Rejected']])
    completed_processes = len([p for p in st.session_state.processes if p['status'] == 'Completed'])
    overdue_processes = len([p for p in st.session_state.processes 
                           if p['status'] not in ['Completed', 'Rejected'] and p['sla_due'] < datetime.now()])
    
    with col1:
        st.metric("Total Processes", total_processes)
    with col2:
        st.metric("Active Processes", active_processes)
    with col3:
        st.metric("Completed Processes", completed_processes)
    with col4:
        st.metric("Overdue Processes", overdue_processes, delta=f"-{overdue_processes}" if overdue_processes > 0 else None)
    
    # Process efficiency analysis
    st.subheader("Process Efficiency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average time per step
        step_times = {}
        steps = get_process_steps()
        for step in steps:
            step_times[step] = 2.5 + len(step) * 0.1  # Mock data
        
        fig_steps = px.bar(x=list(step_times.keys()), 
                          y=list(step_times.values()),
                          title="Average Time per Process Step (Days)",
                          labels={'x': 'Process Step', 'y': 'Average Days'})
        fig_steps.update_xaxes(tickangle=45)
        st.plotly_chart(fig_steps, use_container_width=True)
    
    with col2:
        # Process timeline
        timeline_data = []
        for process in st.session_state.processes:
            days_active = (datetime.now() - process['created_date']).days
            timeline_data.append({
                'Process': process['title'][:20] + '...' if len(process['title']) > 20 else process['title'],
                'Days Active': days_active,
                'Status': process['status'],
                'Current Step': process['current_step']
            })
        
        if timeline_data:
            timeline_df = pd.DataFrame(timeline_data)
            fig_timeline = px.scatter(timeline_df, x='Days Active', y='Process', 
                                    color='Status', size='Days Active',
                                    title="Process Timeline Overview",
                                    hover_data=['Current Step'])
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    # SLA Performance
    st.subheader("SLA Performance Trends")
    
    # Mock trend data
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    sla_compliance = [85 + (i % 10) for i in range(30)]  # Mock data
    
    fig_trend = px.line(x=dates, y=sla_compliance, 
                       title="SLA Compliance Trend (Last 30 Days)",
                       labels={'x': 'Date', 'y': 'SLA Compliance %'})
    fig_trend.add_hline(y=90, line_dash="dash", line_color="red", 
                       annotation_text="Target: 90%")
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Process bottlenecks
    st.subheader("Process Bottleneck Analysis")
    
    bottleneck_data = {
        'PMO Review': 45,
        'Technical Team Review': 30,
        'PMO Validation': 15,
        'Final Approval': 10
    }
    
    fig_bottleneck = px.funnel(y=list(bottleneck_data.keys()), 
                              x=list(bottleneck_data.values()),
                              title="Process Flow - Where Tasks Get Stuck (%)")
    st.plotly_chart(fig_bottleneck, use_container_width=True)

elif page == "➕ New Process Request":
    st.header("New IT Project Request")
    
    if current_user_info['role'] != 'Business User':
        st.warning("Process creation is typically done by Business Users.")
    
    with st.form("new_process_form"):
        st.subheader("Project Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Project Title*", placeholder="Enter project title")
            business_req = st.text_area("Business Requirements*", 
                                      placeholder="Describe the business requirements and objectives")
            timeline = st.selectbox("Estimated Timeline", 
                                   ["1-2 months", "3-4 months", "5-6 months", "6+ months"])
        
        with col2:
            budget = st.selectbox("Estimated Budget", 
                                ["< $25,000", "$25,000 - $50,000", "$50,000 - $100,000", "> $100,000"])
            priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"])
            
            st.subheader("Success Criteria")
            success_criteria = st.text_area("Define success criteria", 
                                          placeholder="How will you measure project success?")
        
        st.subheader("Additional Information")
        stakeholders = st.text_input("Key Stakeholders", 
                                   placeholder="List primary stakeholders and their roles")
        constraints = st.text_area("Known Constraints/Risks", 
                                 placeholder="Any known limitations or risks")
        
        submitted = st.form_submit_button("Submit Process Request")
        
        if submitted:
            if title and business_req:
                process_id = create_new_process(title, business_req, timeline, budget, priority)
                st.success(f"✅ Process request submitted successfully! Process ID: {process_id[:8]}")
                st.info("Your request has been assigned to the PMO team for initial review.")
                
                # Show next steps
                st.subheader("What happens next?")
                st.write("1. **PMO Review** - The PMO team will review your submission and validate requirements")
                st.write("2. **Technical Assessment** - Technical team will evaluate feasibility and provide estimates")
                st.write("3. **PMO Validation** - PMO will ensure alignment between business and technical requirements")
                st.write("4. **Final Approval** - Management will make the final decision")
                
                st.write("You can track the progress of your request in the Work Management System.")
            else:
                st.error("Please fill in all required fields marked with *")

elif page == "🔧 Process Templates":
    st.header("Process Template Management")
    
    if current_user_info['role'] not in ['Manager', 'PMO']:
        st.warning("This section is restricted to Managers and PMO users.")
    else:
        tab1, tab2, tab3 = st.tabs(["📋 Available Templates", "➕ Create Template", "📊 Template Analytics"])
        
        with tab1:
            st.subheader("Available Process Templates")
            
            templates = [
                {"name": "IT Project Request", "steps": 5, "avg_duration": "12 days", "usage": 45, "status": "Active"},
                {"name": "Procurement Request", "steps": 6, "avg_duration": "8 days", "usage": 23, "status": "Active"},
                {"name": "HR Onboarding", "steps": 4, "avg_duration": "5 days", "usage": 12, "status": "Draft"},
                {"name": "Budget Approval", "steps": 3, "avg_duration": "3 days", "usage": 67, "status": "Active"}
            ]
            
            for template in templates:
                with st.expander(f"📄 {template['name']} ({template['status']})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Steps", template['steps'])
                    with col2:
                        st.metric("Avg Duration", template['avg_duration'])
                    with col3:
                        st.metric("Monthly Usage", template['usage'])
                    
                    if st.button(f"Edit {template['name']}", key=f"edit_{template['name']}"):
                        st.info("Template editing interface would open here")
        
        with tab2:
            st.subheader("Create New Process Template")
            
            with st.form("new_template"):
                template_name = st.text_input("Template Name")
                template_desc = st.text_area("Description")
                
                st.write("**Define Process Steps:**")
                num_steps = st.number_input("Number of Steps", min_value=1, max_value=10, value=3)
                
                steps = []
                for i in range(num_steps):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        step_name = st.text_input(f"Step {i+1} Name", key=f"step_name_{i}")
                    with col2:
                        step_role = st.selectbox(f"Assigned Role", ["PMO", "Manager", "Technical Lead", "Business User"], key=f"step_role_{i}")
                    with col3:
                        step_sla = st.number_input(f"SLA (days)", min_value=1, max_value=30, value=3, key=f"step_sla_{i}")
                    
                    if step_name:
                        steps.append({"name": step_name, "role": step_role, "sla": step_sla})
                
                if st.form_submit_button("Create Template"):
                    if template_name and len(steps) > 0:
                        st.success(f"Template '{template_name}' created successfully!")
                    else:
                        st.error("Please provide template name and at least one step")
        
        with tab3:
            st.subheader("Template Performance Analytics")
            
            # Template usage chart
            template_data = pd.DataFrame({
                'Template': ['IT Project', 'Procurement', 'HR Onboarding', 'Budget Approval'],
                'Usage': [45, 23, 12, 67],
                'Avg Completion Time': [12, 8, 5, 3],
                'Success Rate': [85, 92, 98, 78]
            })
            
            col1, col2 = st.columns(2)
            with col1:
                fig_usage = px.bar(template_data, x='Template', y='Usage', title="Template Usage (Monthly)")
                st.plotly_chart(fig_usage, use_container_width=True)
            
            with col2:
                fig_success = px.bar(template_data, x='Template', y='Success Rate', title="Template Success Rate (%)")
                st.plotly_chart(fig_success, use_container_width=True)

elif page == "👤 User Management":
    st.header("User & Role Management")
    
    if current_user_info['role'] != 'Manager':
        st.warning("This section is restricted to Managers.")
    else:
        tab1, tab2, tab3 = st.tabs(["👥 Users", "🔐 Roles & Permissions", "📊 User Analytics"])
        
        with tab1:
            st.subheader("User Management")
            
            # Add new user
            with st.expander("➕ Add New User"):
                with st.form("add_user"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Full Name")
                        new_email = st.text_input("Email")
                    with col2:
                        new_role = st.selectbox("Role", ["Business User", "PMO", "Technical Lead", "Manager"])
                        new_dept = st.selectbox("Department", ["IT", "Marketing", "Finance", "HR", "Operations"])
                    
                    if st.form_submit_button("Add User"):
                        if new_name and new_email:
                            user_id = f"{new_name.lower().replace(' ', '_')}"
                            st.session_state.users[user_id] = {
                                'name': new_name,
                                'role': new_role,
                                'department': new_dept,
                                'email': new_email
                            }
                            st.success(f"User {new_name} added successfully!")
                            st.rerun()
            
            # User list
            st.subheader("Current Users")
            user_data = []
            for user_id, user_info in st.session_state.users.items():
                assigned_tasks = len([p for p in st.session_state.processes if p['assigned_to'] == user_id])
                user_data.append({
                    'Name': user_info['name'],
                    'Role': user_info['role'],
                    'Department': user_info['department'],
                    'Active Tasks': assigned_tasks,
                    'Status': 'Active'
                })
            
            user_df = pd.DataFrame(user_data)
            st.dataframe(user_df, use_container_width=True)
        
        with tab2:
            st.subheader("Role Configuration")
            
            roles_permissions = {
                'Business User': ['Submit Requests', 'View Own Tasks', 'Update Task Status'],
                'PMO': ['Review Requests', 'Assign Tasks', 'View All Tasks', 'Generate Reports'],
                'Technical Lead': ['Technical Review', 'Resource Planning', 'View Team Tasks'],
                'Manager': ['Final Approval', 'User Management', 'System Configuration', 'All Permissions']
            }
            
            for role, permissions in roles_permissions.items():
                with st.expander(f"🔐 {role} Permissions"):
                    for perm in permissions:
                        st.write(f"✓ {perm}")
        
        with tab3:
            st.subheader("User Activity Analytics")
            
            # User productivity metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Tasks completed by user
                user_completion = {}
                for process in st.session_state.processes:
                    if process['status'] == 'Completed':
                        assigned_user = st.session_state.users.get(process['assigned_to'], {}).get('name', 'Unknown')
                        user_completion[assigned_user] = user_completion.get(assigned_user, 0) + 1
                
                if user_completion:
                    fig_completion = px.bar(x=list(user_completion.keys()), y=list(user_completion.values()),
                                          title="Tasks Completed by User")
                    st.plotly_chart(fig_completion, use_container_width=True)
            
            with col2:
                # Department workload
                dept_workload = {}
                for user_id, user_info in st.session_state.users.items():
                    dept = user_info['department']
                    assigned = len([p for p in st.session_state.processes if p['assigned_to'] == user_id])
                    dept_workload[dept] = dept_workload.get(dept, 0) + assigned
                
                fig_dept = px.pie(values=list(dept_workload.values()), names=list(dept_workload.keys()),
                                title="Workload by Department")
                st.plotly_chart(fig_dept, use_container_width=True)

elif page == "📈 Advanced Analytics":
    st.header("Advanced Process Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Process Mining", "📊 Predictive Analytics", "🎯 Performance Benchmarks", "📋 Custom Reports"])
    
    with tab1:
        st.subheader("Process Mining & Flow Analysis")
        
        # Process flow visualization
        st.write("**Process Flow Efficiency:**")
        
        flow_data = {
            'From': ['Start', 'PMO Review', 'Technical Review', 'PMO Validation', 'Final Approval'],
            'To': ['PMO Review', 'Technical Review', 'PMO Validation', 'Final Approval', 'Completed'],
            'Count': [100, 85, 78, 75, 70],
            'Avg_Time': [0, 3.2, 5.1, 2.8, 1.5]
        }
        
        # Sankey diagram would be ideal here
        col1, col2 = st.columns(2)
        
        with col1:
            fig_flow = px.bar(x=flow_data['To'], y=flow_data['Count'], 
                            title="Process Step Completion Rates")
            st.plotly_chart(fig_flow, use_container_width=True)
        
        with col2:
            fig_time = px.bar(x=flow_data['To'], y=flow_data['Avg_Time'],
                            title="Average Time per Step (Days)")
            st.plotly_chart(fig_time, use_container_width=True)
        
        # Bottleneck analysis
        st.subheader("Bottleneck Identification")
        bottlenecks = [
            {"Step": "Technical Review", "Avg Delay": "2.3 days", "Frequency": "45%", "Impact": "High"},
            {"Step": "PMO Review", "Avg Delay": "1.8 days", "Frequency": "30%", "Impact": "Medium"},
            {"Step": "Final Approval", "Avg Delay": "1.2 days", "Frequency": "25%", "Impact": "Low"}
        ]
        
        bottleneck_df = pd.DataFrame(bottlenecks)
        st.dataframe(bottleneck_df, use_container_width=True)
    
    with tab2:
        st.subheader("Predictive Analytics")
        
        # Predicted completion times
        st.write("**Completion Time Predictions:**")
        
        predictions = []
        for process in st.session_state.processes:
            if process['status'] not in ['Completed', 'Rejected']:
                remaining_steps = len(get_process_steps()) - len(process['steps_completed'])
                predicted_days = remaining_steps * 3.5  # Mock calculation
                
                predictions.append({
                    'Process': process['title'],
                    'Current Step': process['current_step'],
                    'Remaining Steps': remaining_steps,
                    'Predicted Completion': (datetime.now() + timedelta(days=predicted_days)).strftime('%Y-%m-%d'),
                    'Confidence': f"{85 + (remaining_steps * 2)}%"
                })
        
        if predictions:
            pred_df = pd.DataFrame(predictions)
            st.dataframe(pred_df, use_container_width=True)
        
        # Risk prediction
        st.subheader("Risk Assessment")
        st.warning("🚨 High Risk: 2 processes predicted to exceed SLA")
        st.info("⚠️ Medium Risk: 3 processes approaching SLA limits")
        st.success("✅ Low Risk: 5 processes on track")
    
    with tab3:
        st.subheader("Performance Benchmarks")
        
        # Industry benchmarks comparison
        benchmark_data = {
            'Metric': ['Avg Process Time', 'SLA Compliance', 'First-Pass Success', 'Customer Satisfaction'],
            'Our Performance': [8.5, 87, 76, 4.2],
            'Industry Average': [12.3, 82, 68, 3.8],
            'Best in Class': [6.2, 95, 89, 4.7],
            'Unit': ['Days', '%', '%', '/5']
        }
        
        benchmark_df = pd.DataFrame(benchmark_data)
        
        # Create comparison chart
        fig_benchmark = go.Figure(data=[
            go.Bar(name='Our Performance', x=benchmark_data['Metric'], y=benchmark_data['Our Performance']),
            go.Bar(name='Industry Average', x=benchmark_data['Metric'], y=benchmark_data['Industry Average']),
            go.Bar(name='Best in Class', x=benchmark_data['Metric'], y=benchmark_data['Best in Class'])
        ])
        fig_benchmark.update_layout(title="Performance Benchmarking", barmode='group')
        st.plotly_chart(fig_benchmark, use_container_width=True)
        
        # Improvement recommendations
        st.subheader("Improvement Recommendations")
        st.write("🎯 **Focus Areas for Improvement:**")
        st.write("1. **Technical Review Step** - Consider parallel reviews to reduce cycle time")
        st.write("2. **SLA Compliance** - Implement automated escalation at 80% of SLA time")
        st.write("3. **First-Pass Success** - Add validation checkpoints in PMO review")
    
    with tab4:
        st.subheader("Custom Report Builder")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**Report Configuration:**")
            report_type = st.selectbox("Report Type", [
                "Process Performance",
                "User Productivity", 
                "SLA Compliance",
                "Department Analysis",
                "Custom Query"
            ])
            
            date_range = st.date_input("Date Range", value=[datetime.now() - timedelta(days=30), datetime.now()])
            
            filters = st.multiselect("Filters", [
                "Department", "Process Type", "Priority", "Status", "Assigned User"
            ])
            
            if st.button("Generate Report"):
                st.success("Report generated successfully!")
        
        with col2:
            st.write("**Sample Report Output:**")
            
            # Mock report data
            report_data = {
                'Process ID': ['PR001', 'PR002', 'PR003', 'PR004'],
                'Title': ['Customer Portal', 'Data Analytics', 'Mobile App', 'Security Audit'],
                'Duration': [12, 8, 15, 6],
                'SLA Status': ['Met', 'Exceeded', 'Met', 'Met'],
                'Rating': [4.2, 4.8, 3.9, 4.5]
            }
            
            report_df = pd.DataFrame(report_data)
            st.dataframe(report_df, use_container_width=True)
            
            # Export options
            st.download_button(
                label="📥 Export to CSV",
                data=report_df.to_csv(index=False),
                file_name="bpm_report.csv",
                mime="text/csv"
            )

elif page == "🔗 System Integrations":
    st.header("System Integration Management")
    
    if current_user_info['role'] not in ['Manager', 'Technical Lead']:
        st.warning("This section is restricted to Managers and Technical Leads.")
    else:
        tab1, tab2, tab3 = st.tabs(["🔌 Active Integrations", "➕ Add Integration", "📊 Integration Health"])
        
        with tab1:
            st.subheader("Current System Integrations")
            
            integrations = [
                {"System": "Salesforce CRM", "Type": "Customer Data", "Status": "🟢 Active", "Last Sync": "2 min ago", "Records": "1,247"},
                {"System": "SAP ERP", "Type": "Financial Data", "Status": "🟡 Warning", "Last Sync": "15 min ago", "Records": "892"},
                {"System": "Jira", "Type": "Project Management", "Status": "🟢 Active", "Last Sync": "1 min ago", "Records": "156"},
                {"System": "Office 365", "Type": "Email/Calendar", "Status": "🔴 Error", "Last Sync": "2 hours ago", "Records": "0"}
            ]
            
            for integration in integrations:
                with st.expander(f"{integration['System']} - {integration['Status']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Type:** {integration['Type']}")
                        st.write(f"**Status:** {integration['Status']}")
                    with col2:
                        st.write(f"**Last Sync:** {integration['Last Sync']}")
                        st.write(f"**Records:** {integration['Records']}")
                    with col3:
                        if st.button(f"Test Connection", key=f"test_{integration['System']}"):
                            st.success("Connection test successful!")
                        if st.button(f"Force Sync", key=f"sync_{integration['System']}"):
                            st.info("Synchronization initiated...")
        
        with tab2:
            st.subheader("Add New Integration")
            
            with st.form("new_integration"):
                system_name = st.text_input("System Name")
                system_type = st.selectbox("Integration Type", [
                    "CRM", "ERP", "Project Management", "HR System", "Email", "Database", "Custom API"
                ])
                
                st.write("**Connection Details:**")
                col1, col2 = st.columns(2)
                with col1:
                    endpoint = st.text_input("API Endpoint")
                    auth_type = st.selectbox("Authentication", ["API Key", "OAuth", "Basic Auth", "Token"])
                with col2:
                    sync_frequency = st.selectbox("Sync Frequency", ["Real-time", "Every 5 min", "Hourly", "Daily"])
                    data_direction = st.selectbox("Data Flow", ["Bidirectional", "Import Only", "Export Only"])
                
                if st.form_submit_button("Add Integration"):
                    if system_name and endpoint:
                        st.success(f"Integration with {system_name} configured successfully!")
                    else:
                        st.error("Please fill in required fields")
        
        with tab3:
            st.subheader("Integration Health Dashboard")
            
            # Integration performance metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Active Integrations", "4")
            with col2:
                st.metric("Sync Success Rate", "96.7%", "↗️ +2.1%")
            with col3:
                st.metric("Avg Response Time", "145ms", "↘️ -23ms")
            with col4:
                st.metric("Data Records/Hour", "12.4K", "↗️ +1.2K")
            
            # Sync status over time
            dates = pd.date_range(start=datetime.now()-timedelta(days=7), end=datetime.now(), freq='H')
            sync_success = [95 + (i % 10) for i in range(len(dates))]
            
            fig_sync = px.line(x=dates, y=sync_success, title="Integration Sync Success Rate (7 Days)")
            fig_sync.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="SLA: 95%")
            st.plotly_chart(fig_sync, use_container_width=True)

elif page == "⚙️ SLA Configuration":
    st.header("SLA Configuration & Management")
    
    if current_user_info['role'] not in ['Manager', 'PMO']:
        st.warning("This section is restricted to Managers and PMO users.")
    else:
        tab1, tab2, tab3 = st.tabs(["📋 SLA Rules", "🚨 Escalation Matrix", "📊 SLA Performance"])
        
        with tab1:
            st.subheader("SLA Rule Configuration")
            
            # Current SLA rules
            sla_rules = [
                {"Process": "IT Project Request", "Step": "PMO Review", "SLA": "3 days", "Warning": "2 days", "Critical": "2.5 days"},
                {"Process": "IT Project Request", "Step": "Technical Review", "SLA": "5 days", "Warning": "3 days", "Critical": "4 days"},
                {"Process": "IT Project Request", "Step": "PMO Validation", "SLA": "2 days", "Warning": "1 day", "Critical": "1.5 days"},
                {"Process": "IT Project Request", "Step": "Final Approval", "SLA": "3 days", "Warning": "2 days", "Critical": "2.5 days"},
                {"Process": "Procurement", "Step": "Vendor Review", "SLA": "2 days", "Warning": "1 day", "Critical": "1.5 days"}
            ]
            
            sla_df = pd.DataFrame(sla_rules)
            edited_df = st.data_editor(sla_df, use_container_width=True)
            
            if st.button("Save SLA Configuration"):
                st.success("SLA rules updated successfully!")
            
            # Add new SLA rule
            with st.expander("➕ Add New SLA Rule"):
                with st.form("new_sla"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_process = st.text_input("Process Type")
                        new_step = st.text_input("Process Step")
                    with col2:
                        new_sla = st.number_input("SLA (days)", min_value=1, max_value=30, value=3)
                        new_warning = st.number_input("Warning Threshold (days)", min_value=1, max_value=30, value=2)
                    
                    if st.form_submit_button("Add SLA Rule"):
                        if new_process and new_step:
                            st.success("New SLA rule added!")
        
        with tab2:
            st.subheader("Escalation Matrix")
            
            escalation_rules = [
                {"Trigger": "SLA 80% reached", "Action": "Email to assigned user", "Recipients": "Task Owner"},
                {"Trigger": "SLA 90% reached", "Action": "Email to manager", "Recipients": "Task Owner + Manager"},
                {"Trigger": "SLA exceeded", "Action": "Auto-escalate + SMS", "Recipients": "Manager + Department Head"},
                {"Trigger": "SLA exceeded by 50%", "Action": "Executive notification", "Recipients": "C-Level"}
            ]
            
            escalation_df = pd.DataFrame(escalation_rules)
            st.dataframe(escalation_df, use_container_width=True)
            
            # Escalation settings
            st.subheader("Escalation Settings")
            col1, col2 = st.columns(2)
            with col1:
                email_enabled = st.checkbox("Enable Email Notifications", value=True)
                sms_enabled = st.checkbox("Enable SMS Alerts", value=False)
            with col2:
                business_hours = st.checkbox("Business Hours Only", value=True)
                weekend_escalation = st.checkbox("Weekend Escalation", value=False)
        
        with tab3:
            st.subheader("SLA Performance Analysis")
            
            # SLA metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall SLA Compliance", "87.3%", "↗️ +2.1%")
            with col2:
                st.metric("Avg Resolution Time", "6.2 days", "↘️ -0.8 days")
            with col3:
                st.metric("Escalations This Month", "12", "↘️ -3")
            with col4:
                st.metric("Critical SLA Breaches", "2", "↘️ -1")
            
            # SLA performance by step
            step_performance = {
                'Step': ['PMO Review', 'Technical Review', 'PMO Validation', 'Final Approval'],
                'SLA Compliance': [92, 78, 89, 95],
                'Avg Duration': [2.1, 4.8, 1.6, 2.3]
            }
            
            col1, col2 = st.columns(2)
            with col1:
                fig_compliance = px.bar(x=step_performance['Step'], y=step_performance['SLA Compliance'],
                                      title="SLA Compliance by Step (%)")
                fig_compliance.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="Target: 90%")
                st.plotly_chart(fig_compliance, use_container_width=True)
            
            with col2:
                fig_duration = px.bar(x=step_performance['Step'], y=step_performance['Avg Duration'],
                                    title="Average Duration by Step (Days)")
                st.plotly_chart(fig_duration, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**BPM System Demo v1.0**")
st.sidebar.markdown("Built with Streamlit")

# Real-time updates simulation
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()