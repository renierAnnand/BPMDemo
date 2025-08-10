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

# Custom CSS for styling (enhanced for WMS look)
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 28px;
        margin-bottom: 30px;
        color: white;
    }
    
    /* Process card styling */
    .process-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Status badges */
    .status-active {
        background: #c6f6d5;
        color: #22543d;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        display: inline-block;
    }
    
    .status-beta {
        background: #fed7d7;
        color: #742a2a;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        display: inline-block;
    }
    
    .status-new {
        background: #bee3f8;
        color: #2a4365;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        display: inline-block;
    }
    
    /* Table styling for WMS */
    .wms-header {
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        padding: 12px;
        display: flex;
        text-align: center;
        border-radius: 5px 5px 0 0;
    }
    
    .wms-row {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #ddd;
        background-color: white;
    }
    
    .wms-row:hover {
        background-color: #f8f9fa;
    }
    
    /* Status colors for tasks */
    .status-pending {
        background-color: #FFF3CD !important;
        color: #856404 !important;
        font-weight: bold !important;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .status-progress {
        background-color: #D4EDDA !important;
        color: #155724 !important;
        font-weight: bold !important;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .status-completed {
        background-color: #D1ECF1 !important;
        color: #0C5460 !important;
        font-weight: bold !important;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .status-rejected {
        background-color: #F8D7DA !important;
        color: #721C24 !important;
        font-weight: bold !important;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    /* Priority colors */
    .priority-high {
        color: #DC3545 !important;
        font-weight: bold !important;
    }
    
    .priority-medium {
        color: #FFC107 !important;
        font-weight: bold !important;
    }
    
    .priority-low {
        color: #28A745 !important;
        font-weight: bold !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 35px;
        border-radius: 50%;
        border: none;
        font-size: 16px;
        margin: 2px;
    }
    
    .stButton > button:hover {
        transform: scale(1.1);
        transition: transform 0.2s;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Checklist styling */
    .checklist-item {
        padding: 8px;
        margin: 4px 0;
        border-left: 3px solid #e2e8f0;
        background-color: #f8f9fa;
        border-radius: 4px;
    }
    
    .checklist-item.required {
        border-left-color: #dc3545;
    }
    
    .checklist-item.optional {
        border-left-color: #17a2b8;
    }
    
    .checklist-item.completed {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    
    .checklist-progress {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .step-completion-disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    
    /* Template builder styling */
    .template-step {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    
    .checklist-builder {
        background-color: white;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

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
if 'show_details' not in st.session_state:
    st.session_state.show_details = {}
if 'task_actions' not in st.session_state:
    st.session_state.task_actions = {}
if 'process_templates' not in st.session_state:
    st.session_state.process_templates = {}
if 'checklist_progress' not in st.session_state:
    st.session_state.checklist_progress = {}

# Sample data initialization with detailed task information and checklists
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
            'priority': 'High',
            'description': 'Implement comprehensive customer portal enhancement with new dashboard features and improved user experience.',
            'created_by': 'Marketing Manager',
            'comments': 'Critical for Q3 customer satisfaction initiative.',
            'checklists': {
                'PMO Review': [
                    {'name': 'Business Requirements Document uploaded', 'description': 'Complete BRD with all sections filled', 'required': True, 'completed': True},
                    {'name': 'Stakeholder list confirmed', 'description': 'All stakeholders identified and contacted', 'required': True, 'completed': True},
                    {'name': 'Budget estimate provided', 'description': 'Initial budget estimate documented', 'required': True, 'completed': True}
                ],
                'Technical Team Review': [
                    {'name': 'Feasibility analysis completed', 'description': 'Technical feasibility assessment done', 'required': True, 'completed': False},
                    {'name': 'Time and effort estimation added', 'description': 'Development timeline estimated', 'required': True, 'completed': False},
                    {'name': 'Resource allocation reviewed', 'description': 'Team resources confirmed available', 'required': True, 'completed': False}
                ]
            }
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
            'priority': 'Medium',
            'description': 'Deploy enterprise-wide data analytics platform for business intelligence and reporting.',
            'created_by': 'IT Director',
            'comments': 'Requires board approval due to budget size.',
            'checklists': {
                'Final Approval': [
                    {'name': 'Budget approval from CFO', 'description': 'CFO sign-off on budget allocation', 'required': True, 'completed': False},
                    {'name': 'Board resolution signed', 'description': 'Board approval documented', 'required': True, 'completed': False},
                    {'name': 'Compliance review completed', 'description': 'Legal and compliance check done', 'required': False, 'completed': True}
                ]
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Employee Onboarding System',
            'type': 'HR Process',
            'submitter': 'sarah_pmo',
            'created_date': datetime.now() - timedelta(days=3),
            'current_step': 'PMO Review',
            'assigned_to': 'sarah_pmo',
            'status': 'Pending',
            'sla_due': datetime.now() + timedelta(days=4),
            'steps_completed': ['Business User Submission'],
            'business_requirements': 'Automate new employee onboarding process',
            'timeline': '2 months',
            'budget': '$25,000',
            'priority': 'Medium',
            'description': 'Streamline new hire onboarding with automated workflows and document collection.',
            'created_by': 'HR Manager',
            'comments': 'Part of digital transformation initiative.',
            'checklists': {
                'PMO Review': [
                    {'name': 'HR requirements documented', 'description': 'All HR workflow requirements captured', 'required': True, 'completed': True},
                    {'name': 'Integration points identified', 'description': 'HRIS and other system integrations mapped', 'required': True, 'completed': False},
                    {'name': 'Compliance requirements reviewed', 'description': 'Legal compliance for employee data handling', 'required': True, 'completed': False}
                ]
            }
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Procurement Workflow Automation',
            'type': 'Procurement Process',
            'submitter': 'john_doe',
            'created_date': datetime.now() - timedelta(days=1),
            'current_step': 'Business User Submission',
            'assigned_to': 'sarah_pmo',
            'status': 'Completed',
            'sla_due': datetime.now() + timedelta(days=5),
            'steps_completed': ['Business User Submission', 'PMO Review', 'Technical Team Review', 'PMO Validation', 'Final Approval'],
            'business_requirements': 'Automate procurement approval workflow',
            'timeline': '4 months',
            'budget': '$75,000',
            'priority': 'High',
            'description': 'Implement end-to-end procurement workflow automation with vendor integration.',
            'created_by': 'Procurement Manager',
            'comments': 'Successfully deployed and operational.',
            'checklists': {}
        }
    ]
    st.session_state.processes.extend(sample_processes)

# Initialize default process templates with checklists
if not st.session_state.process_templates:
    st.session_state.process_templates = {
        'IT Project Request': {
            'steps': [
                {
                    'name': 'PMO Review',
                    'role': 'PMO',
                    'sla_days': 3,
                    'checklist': [
                        {'name': 'Business Requirements Collection', 'description': 'Ensure business user provides detailed project description', 'required': True},
                        {'name': 'Functional and Non-Functional Requirements', 'description': 'Clarify and document functional requirements', 'required': True},
                        {'name': 'Stakeholder Identification', 'description': 'Confirm list of stakeholders and their roles', 'required': True},
                        {'name': 'Timeline and Budget Estimates', 'description': 'Verify timeline and budget estimates provided', 'required': True},
                        {'name': 'Risks and Constraints', 'description': 'Identify any risks that could impact the project', 'required': False}
                    ]
                },
                {
                    'name': 'Technical Team Review',
                    'role': 'Technical Lead',
                    'sla_days': 5,
                    'checklist': [
                        {'name': 'Feasibility Analysis', 'description': 'Assess technical feasibility of the project', 'required': True},
                        {'name': 'Resource Estimation', 'description': 'Estimate development time and team resources', 'required': True},
                        {'name': 'Architecture Review', 'description': 'Review technical architecture and approach', 'required': True},
                        {'name': 'Integration Assessment', 'description': 'Assess integration requirements with existing systems', 'required': False}
                    ]
                },
                {
                    'name': 'PMO Validation',
                    'role': 'PMO',
                    'sla_days': 2,
                    'checklist': [
                        {'name': 'Business-Technical Alignment', 'description': 'Ensure technical solution aligns with business requirements', 'required': True},
                        {'name': 'Timeline Validation', 'description': 'Validate realistic timeline based on technical assessment', 'required': True},
                        {'name': 'Budget Reconciliation', 'description': 'Reconcile final budget with technical estimates', 'required': True}
                    ]
                },
                {
                    'name': 'Final Approval',
                    'role': 'Manager',
                    'sla_days': 3,
                    'checklist': [
                        {'name': 'Executive Review', 'description': 'Present project proposal to executive team', 'required': True},
                        {'name': 'Budget Approval', 'description': 'Obtain budget approval from finance', 'required': True},
                        {'name': 'Resource Commitment', 'description': 'Confirm resource allocation and availability', 'required': True}
                    ]
                }
            ]
        }
    }

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

def create_new_process(title, business_req, timeline, budget, priority, process_type='IT Project Request'):
    process_id = str(uuid.uuid4())
    
    # Get checklist template if available
    checklists = {}
    if process_type in st.session_state.process_templates:
        template = st.session_state.process_templates[process_type]
        for step in template['steps']:
            step_name = step['name']
            checklists[step_name] = []
            for item in step.get('checklist', []):
                checklists[step_name].append({
                    'name': item['name'],
                    'description': item.get('description', ''),
                    'required': item.get('required', True),
                    'completed': False
                })
    
    new_process = {
        'id': process_id,
        'title': title,
        'type': process_type,
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
        'priority': priority,
        'description': business_req,
        'created_by': st.session_state.users[st.session_state.current_user]['name'],
        'comments': 'Newly submitted request awaiting review.',
        'checklists': checklists
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
    "🏢 SmartProcess Hub",
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
    st.markdown('<div class="main-title">📋 Work Management System</div>', unsafe_allow_html=True)
    
    # Filter processes for current user or show all if manager
    if current_user_info['role'] in ['Manager', 'PMO']:
        user_processes = st.session_state.processes
        st.info("👥 Showing all processes (Manager/PMO View)")
    else:
        user_processes = []
        for process in st.session_state.processes:
            if (process['assigned_to'] == st.session_state.current_user or 
                process['submitter'] == st.session_state.current_user):
                user_processes.append(process)
        st.info("👤 Showing your assigned and submitted processes")
    
    if not user_processes:
        st.info("No tasks assigned to you currently.")
    else:
        # Create WMS-style table header
        st.markdown("""
        <div class="wms-header">
            <div style="flex: 0.5; border-right: 1px solid white; padding: 8px;">#</div>
            <div style="flex: 3; border-right: 1px solid white; padding: 8px;">Task</div>
            <div style="flex: 1.5; border-right: 1px solid white; padding: 8px;">Type</div>
            <div style="flex: 1.5; border-right: 1px solid white; padding: 8px;">Status</div>
            <div style="flex: 2; border-right: 1px solid white; padding: 8px;">Assigned to</div>
            <div style="flex: 1; border-right: 1px solid white; padding: 8px;">Priority</div>
            <div style="flex: 1.5; padding: 8px;">Action</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each row with WMS styling
        for index, process in enumerate(user_processes, 1):
            process_id = process['id']
            task_name = process['title']
            task_type = process['type']
            status = process['status']
            assigned_user = st.session_state.users.get(process['assigned_to'], {}).get('name', 'Unknown')
            priority = process['priority']
            
            # Determine status color class
            status_class = {
                "Pending": "status-pending",
                "Pending Approval": "status-pending",
                "In Progress": "status-progress", 
                "Completed": "status-completed",
                "Rejected": "status-rejected"
            }.get(status, "")
            
            # Determine priority color
            priority_color = {
                "High": "#DC3545",
                "Medium": "#FFC107",
                "Low": "#28A745"
            }.get(priority, "#000000")
            
            # Create columns for the row
            cols = st.columns([0.5, 3, 1.5, 1.5, 2, 1, 1.5])
            
            with cols[0]:
                st.markdown(f"<div style='text-align: center; padding: 10px; border-bottom: 1px solid #ddd;'>{index}</div>", unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown(f"<div style='text-align: center; padding: 10px; border-bottom: 1px solid #ddd;'>{task_name}</div>", unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown(f"<div style='text-align: center; padding: 10px; border-bottom: 1px solid #ddd;'>{task_type}</div>", unsafe_allow_html=True)
            
            with cols[3]:
                st.markdown(f"<div style='text-align: center; padding: 10px; border-bottom: 1px solid #ddd;'><span class='{status_class}'>{status}</span></div>", unsafe_allow_html=True)
            
            with cols[4]:
                st.markdown(f"<div style='text-align: center; padding: 10px; border-bottom: 1px solid #ddd;'>{assigned_user}</div>", unsafe_allow_html=True)
            
            with cols[5]:
                st.markdown(f"<div style='text-align: center; padding: 10px; border-bottom: 1px solid #ddd; color: {priority_color}; font-weight: bold;'>{priority}</div>", unsafe_allow_html=True)
            
            with cols[6]:
                # Action buttons
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    if st.button("👁️", key=f"view_{process_id}", help="View Details"):
                        st.session_state.show_details[process_id] = not st.session_state.show_details.get(process_id, False)
                
                with btn_cols[1]:
                    if st.button("✅", key=f"action_{process_id}", help="Take Action"):
                        st.session_state.task_actions[process_id] = not st.session_state.task_actions.get(process_id, False)

    # Display task details if view button was clicked
    for process_id in st.session_state.show_details:
        if st.session_state.show_details[process_id]:
            process = next((p for p in st.session_state.processes if p['id'] == process_id), None)
            if process:
                with st.expander(f"📋 Task Details - {process['title']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Description:** {process['description']}")
                        st.write(f"**Due Date:** {process['sla_due'].strftime('%Y-%m-%d %H:%M')}")
                        st.write(f"**Timeline:** {process['timeline']}")
                        st.write(f"**Budget:** {process['budget']}")
                    
                    with col2:
                        st.write(f"**Created By:** {process['created_by']}")
                        st.write(f"**Current Step:** {process['current_step']}")
                        st.write(f"**Created Date:** {process['created_date'].strftime('%Y-%m-%d')}")
                        st.write(f"**Comments:** {process['comments']}")
                    
                    # Progress indicator
                    st.subheader("Progress:")
                    steps = get_process_steps()
                    progress_cols = st.columns(len(steps))
                    for i, step in enumerate(steps):
                        with progress_cols[i]:
                            if step in process['steps_completed']:
                                st.markdown(f"<div style='text-align: center; color: green;'>✅<br>{step}</div>", unsafe_allow_html=True)
                            elif step == process['current_step']:
                                st.markdown(f"<div style='text-align: center; color: orange;'>🔄<br>{step}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div style='text-align: center; color: gray;'>⏳<br>{step}</div>", unsafe_allow_html=True)
                    
                    if st.button("Close Details", key=f"close_{process_id}"):
                        st.session_state.show_details[process_id] = False
                        st.rerun()

    # Display action forms if action button was clicked
    for process_id in st.session_state.task_actions:
        if st.session_state.task_actions[process_id]:
            process = next((p for p in st.session_state.processes if p['id'] == process_id), None)
            if process:
                with st.expander(f"⚡ Take Action on Task - {process['title']}", expanded=True):
                    st.write(f"**Task:** {process['title']}")
                    st.write(f"**Current Status:** {process['status']}")
                    
                    # Display checklist for current step if available
                    current_step = process['current_step']
                    if 'checklists' in process and current_step in process['checklists']:
                        st.write(f"**{current_step} Checklist:**")
                        
                        checklist_items = process['checklists'][current_step]
                        all_required_completed = True
                        
                        for i, item in enumerate(checklist_items):
                            item_key = f"checklist_{process['id']}_{current_step}_{i}"
                            
                            # Display checklist item
                            col_check, col_details = st.columns([1, 4])
                            
                            with col_check:
                                item_completed = st.checkbox(
                                    "",
                                    value=item.get('completed', False),
                                    key=item_key,
                                    help=f"{'Required' if item['required'] else 'Optional'}"
                                )
                                # Update completion status
                                item['completed'] = item_completed
                            
                            with col_details:
                                required_indicator = "🔴" if item['required'] else "🔵"
                                st.write(f"{required_indicator} **{item['name']}**")
                                if item.get('description'):
                                    st.caption(item['description'])
                            
                            # Check if required items are completed
                            if item['required'] and not item_completed:
                                all_required_completed = False
                        
                        # Completion status indicator
                        if all_required_completed:
                            st.success("✅ All required checklist items completed!")
                        else:
                            st.warning("⚠️ Complete all required checklist items to proceed")
                    
                    # Legacy action handling for processes without checklists
                    if process['current_step'] == 'PMO Review' and current_user_info['role'] == 'PMO':
                        if 'checklists' not in process or 'PMO Review' not in process['checklists']:
                            # Legacy checklist for backward compatibility
                            st.write("**PMO Review Checklist:**")
                            req_collected = st.checkbox("✓ Business Requirements Collection", key=f"req_{process['id']}")
                            func_req = st.checkbox("✓ Functional and Non-Functional Requirements", key=f"func_{process['id']}")
                            stakeholders = st.checkbox("✓ Stakeholder Identification", key=f"stake_{process['id']}")
                            timeline_check = st.checkbox("✓ Timeline and Budget Estimates", key=f"time_{process['id']}")
                            risks = st.checkbox("✓ Risks and Constraints", key=f"risk_{process['id']}")
                            all_required_completed = all([req_collected, func_req, stakeholders, timeline_check, risks])
                        
                        # Complete step button
                        step_complete_disabled = not all_required_completed if ('checklists' in process and 'PMO Review' in process['checklists']) else not all([req_collected, func_req, stakeholders, timeline_check, risks]) if 'checklists' not in process or 'PMO Review' not in process['checklists'] else False
                        
                        if st.button(f"Complete PMO Review", key=f"complete_pmo_{process['id']}", disabled=step_complete_disabled):
                            process['current_step'] = 'Technical Team Review'
                            process['assigned_to'] = 'mike_tech'
                            process['steps_completed'].append('PMO Review')
                            process['sla_due'] = datetime.now() + timedelta(days=5)
                            st.success("PMO Review completed! Task moved to Technical Team.")
                            st.rerun()
                    
                    elif process['current_step'] == 'Technical Team Review' and current_user_info['role'] == 'Technical Lead':
                        if 'checklists' not in process or 'Technical Team Review' not in process['checklists']:
                            st.write("**Technical Review:**")
                            feasibility = st.selectbox("Project Feasibility", 
                                                     ["Select", "Feasible", "Needs Modification", "Not Feasible"],
                                                     key=f"feas_{process['id']}")
                            effort = st.text_input("Estimated Effort (hours)", key=f"effort_{process['id']}")
                            all_required_completed = feasibility != "Select" and effort
                        
                        step_complete_disabled = not all_required_completed
                        
                        if st.button(f"Complete Technical Review", key=f"complete_tech_{process['id']}", disabled=step_complete_disabled):
                            process['current_step'] = 'PMO Validation'
                            process['assigned_to'] = 'sarah_pmo'
                            process['steps_completed'].append('Technical Team Review')
                            process['sla_due'] = datetime.now() + timedelta(days=2)
                            st.success("Technical Review completed! Task moved back to PMO for validation.")
                            st.rerun()
                    
                    elif process['current_step'] == 'PMO Validation' and current_user_info['role'] == 'PMO':
                        if 'checklists' not in process or 'PMO Validation' not in process['checklists']:
                            st.write("**PMO Validation:**")
                            alignment = st.selectbox("Business-Technical Alignment", 
                                                    ["Select", "Aligned", "Minor Adjustments Needed", "Major Revisions Required"],
                                                    key=f"align_{process['id']}")
                            all_required_completed = alignment != "Select"
                        
                        step_complete_disabled = not all_required_completed
                        
                        if st.button(f"Complete PMO Validation", key=f"complete_val_{process['id']}", disabled=step_complete_disabled):
                            process['current_step'] = 'Final Approval'
                            process['assigned_to'] = 'lisa_manager'
                            process['steps_completed'].append('PMO Validation')
                            process['sla_due'] = datetime.now() + timedelta(days=3)
                            st.success("PMO Validation completed! Task moved to Final Approval.")
                            st.rerun()
                    
                    elif process['current_step'] == 'Final Approval' and current_user_info['role'] == 'Manager':
                        if 'checklists' not in process or 'Final Approval' not in process['checklists']:
                            st.write("**Final Approval:**")
                            decision = st.selectbox("Approval Decision", 
                                                   ["Select", "Approved", "Approved with Conditions", "Rejected"],
                                                   key=f"decision_{process['id']}")
                            all_required_completed = decision != "Select"
                        
                        step_complete_disabled = not all_required_completed
                        
                        if st.button(f"Make Final Decision", key=f"complete_final_{process['id']}", disabled=step_complete_disabled):
                            process['steps_completed'].append('Final Approval')
                            process['status'] = 'Completed' if 'checklists' not in process or decision == 'Approved' else 'Rejected'
                            process['current_step'] = 'Completed'
                            st.success(f"Process completed!")
                            st.rerun()
                    
                    # Generic completion button for steps with checklists
                    elif 'checklists' in process and current_step in process['checklists']:
                        step_complete_disabled = not all_required_completed
                        
                        if st.button(f"Complete {current_step}", key=f"complete_step_{process['id']}", disabled=step_complete_disabled):
                            # Move to next step logic here
                            steps = get_process_steps()
                            current_index = steps.index(current_step) if current_step in steps else -1
                            
                            if current_index < len(steps) - 1:
                                next_step = steps[current_index + 1]
                                process['current_step'] = next_step
                                process['steps_completed'].append(current_step)
                                
                                # Assign to appropriate user based on step
                                if 'Technical' in next_step:
                                    process['assigned_to'] = 'mike_tech'
                                elif 'PMO' in next_step:
                                    process['assigned_to'] = 'sarah_pmo'
                                elif 'Final' in next_step or 'Manager' in next_step:
                                    process['assigned_to'] = 'lisa_manager'
                                
                                process['sla_due'] = datetime.now() + timedelta(days=3)
                                st.success(f"{current_step} completed! Task moved to {next_step}.")
                            else:
                                process['steps_completed'].append(current_step)
                                process['status'] = 'Completed'
                                process['current_step'] = 'Completed'
                                st.success("Process completed successfully!")
                            
                            st.rerun()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_status = st.selectbox(
                            "Update Status:",
                            ["Pending", "In Progress", "Completed", "Rejected"],
                            index=["Pending", "In Progress", "Completed", "Rejected"].index(process['status']) if process['status'] in ["Pending", "In Progress", "Completed", "Rejected"] else 0,
                            key=f"status_{process_id}"
                        )
                    
                    with col2:
                        all_users = [user_info['name'] for user_info in st.session_state.users.values()]
                        current_assignee = st.session_state.users.get(process['assigned_to'], {}).get('name', 'Unknown')
                        new_assignee_name = st.selectbox(
                            "Reassign to:",
                            all_users,
                            index=all_users.index(current_assignee) if current_assignee in all_users else 0,
                            key=f"assignee_{process_id}"
                        )
                    
                    action_comments = st.text_area(
                        "Action Comments:",
                        placeholder="Enter your comments about this action...",
                        key=f"comments_{process_id}"
                    )
                    
                    action_cols = st.columns(3)
                    with action_cols[0]:
                        if st.button("💾 Save Changes", key=f"save_{process_id}"):
                            # Update process
                            process['status'] = new_status
                            process['comments'] = action_comments if action_comments else process['comments']
                            
                            # Find new assignee user ID
                            for user_id, user_info in st.session_state.users.items():
                                if user_info['name'] == new_assignee_name:
                                    process['assigned_to'] = user_id
                                    break
                            
                            st.success(f"✅ Task updated successfully!")
                            st.session_state.task_actions[process_id] = False
                            st.rerun()
                    
                    with action_cols[1]:
                        if st.button("📧 Send Notification", key=f"notify_{process_id}"):
                            st.info(f"📨 Notification sent to {new_assignee_name}")
                    
                    with action_cols[2]:
                        if st.button("❌ Cancel", key=f"cancel_{process_id}"):
                            st.session_state.task_actions[process_id] = False
                            st.rerun()

    # Summary statistics
    st.subheader("📊 Task Summary")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Tasks", len(user_processes))

    with col2:
        pending_count = len([p for p in user_processes if p['status'] in ['Pending', 'Pending Approval']])
        st.metric("Pending", pending_count)

    with col3:
        completed_count = len([p for p in user_processes if p['status'] == 'Completed'])
        st.metric("Completed", completed_count)

    with col4:
        high_priority_count = len([p for p in user_processes if p['priority'] == 'High'])
        st.metric("High Priority", high_priority_count)

elif page == "🏢 SmartProcess Hub":
    st.markdown("""
    <div class="main-title">
        <h1>🏢 SmartProcess Hub</h1>
        <p>Select a process to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Available processes with status indicators
    available_processes = [
        {
            "name": "New Hire Onboarding",
            "icon": "👤",
            "description": "Streamline employee onboarding with automated workflows and document collection.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "IT Project Request",
            "icon": "💻",
            "description": "Submit and track IT project requests with comprehensive approval workflow.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "Expense Report",
            "icon": "💳",
            "description": "Submit and manage expense claims with receipt attachment and approval flow.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "Leave Request",
            "icon": "🏖️",
            "description": "Request time off with calendar integration and manager approval workflow.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "Purchase Order Request",
            "icon": "📋",
            "description": "Submit and track purchase order requests with approval workflow.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "Asset Management",
            "icon": "🖥️",
            "description": "Track and manage company assets with assignment and maintenance schedules.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "Supplier Registration",
            "icon": "🤝",
            "description": "Onboard new suppliers with complete registration and verification process.",
            "status": "new",
            "form_available": False
        },
        {
            "name": "Contract Review",
            "icon": "📄",
            "description": "Submit contracts for legal review with collaborative editing and approval.",
            "status": "beta",
            "form_available": False
        },
        {
            "name": "Performance Review",
            "icon": "⭐",
            "description": "Conduct employee performance evaluations with 360-degree feedback collection.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "Customer/Vendor Creation",
            "icon": "🏢",
            "description": "Register new customers and vendors with comprehensive profile setup and verification.",
            "status": "active",
            "form_available": True
        },
        {
            "name": "Invoice Processing",
            "icon": "💰",
            "description": "Automate invoice validation, approval, and payment processing.",
            "status": "beta",
            "form_available": False
        },
        {
            "name": "Project Initiation",
            "icon": "🚀",
            "description": "Submit new project proposals with budget requests and approval routing.",
            "status": "active",
            "form_available": True
        }
    ]
    
    # Display process cards in a grid layout
    cols_per_row = 3
    for i in range(0, len(available_processes), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < len(available_processes):
                process = available_processes[i + j]
                
                with cols[j]:
                    # Determine status styling
                    if process['status'] == 'active':
                        status_html = '<span class="status-active">Active</span>'
                    elif process['status'] == 'beta':
                        status_html = '<span class="status-beta">Beta</span>'
                    else:
                        status_html = '<span class="status-new">New</span>'
                    
                    st.markdown(f"""
                    <div class="process-card">
                        <div>
                            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{process['icon']}</div>
                            <div class="card-title">{process['name']}</div>
                            <div class="card-description">{process['description']}</div>
                        </div>
                        <div>{status_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if process['form_available']:
                        if st.button(f"Open {process['name']}", key=f"open_{process['name'].replace(' ', '_').lower()}", use_container_width=True):
                            st.success(f"✅ {process['name']} process opened!")
                            st.info("In a full implementation, this would navigate to the specific process form.")
                    else:
                        st.button(f"Coming Soon - {process['name']}", key=f"coming_{process['name'].replace(' ', '_').lower()}", 
                                use_container_width=True, disabled=True)
    
    # Process categories section
    st.subheader("📂 Process Categories")
    
    category_cols = st.columns(4)
    
    with category_cols[0]:
        st.markdown("""
        **👥 HR & Admin**
        - New Hire Onboarding
        - Leave Request
        - Performance Review
        - Asset Management
        """)
    
    with category_cols[1]:
        st.markdown("""
        **💼 Finance & Procurement**
        - Purchase Order Request
        - Expense Report
        - Invoice Processing
        - Contract Review
        """)
    
    with category_cols[2]:
        st.markdown("""
        **🏢 Customer & Vendor**
        - Customer/Vendor Creation
        - Supplier Registration
        - Contract Management
        """)
    
    with category_cols[3]:
        st.markdown("""
        **🚀 Projects & IT**
        - IT Project Request
        - Project Initiation
        - Change Management
        """)

elif page == "👥 Manager's View":
    st.header("Manager's View")
    
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
    st.header("New Process Request")
    
    with st.form("new_process_form"):
        st.subheader("Request Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Process type selection
            available_types = ['IT Project Request'] + list(st.session_state.process_templates.keys())
            process_type = st.selectbox("Process Type*", available_types)
            
            title = st.text_input("Request Title*", placeholder="Enter request title")
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
        
        # Show template preview if selected
        if process_type in st.session_state.process_templates:
            st.subheader(f"📋 {process_type} Process Preview")
            template = st.session_state.process_templates[process_type]
            
            st.write("**This request will follow these steps:**")
            for i, step in enumerate(template['steps'], 1):
                step_name = step.get('name', f"Step {i}")
                step_role = step.get('role', 'N/A')
                step_sla = step.get('sla_days', step.get('sla', 3))
                checklist_count = len(step.get('checklist', []))
                
                st.write(f"{i}. **{step_name}** (Assigned to: {step_role}, SLA: {step_sla} days)")
                if checklist_count > 0:
                    st.write(f"   📋 {checklist_count} checklist items to complete")
        
        st.subheader("Additional Information")
        stakeholders = st.text_input("Key Stakeholders", 
                                   placeholder="List primary stakeholders and their roles")
        constraints = st.text_area("Known Constraints/Risks", 
                                 placeholder="Any known limitations or risks")
        
        submitted = st.form_submit_button("Submit Process Request")
        
        if submitted:
            if title and business_req:
                process_id = create_new_process(title, business_req, timeline, budget, priority, process_type)
                st.success(f"✅ {process_type} request submitted successfully! Process ID: {process_id[:8]}")
                st.info("Your request has been assigned to the appropriate team for initial review.")
                
                # Show next steps based on template
                if process_type in st.session_state.process_templates:
                    template = st.session_state.process_templates[process_type]
                    st.subheader("What happens next?")
                    for i, step in enumerate(template['steps'], 1):
                        step_name = step.get('name', f"Step {i}")
                        step_role = step.get('role', 'N/A')
                        st.write(f"{i}. **{step_name}** - The {step_role} team will review your submission")
                else:
                    # Default next steps
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
    
    tab1, tab2, tab3 = st.tabs(["📋 Available Templates", "➕ Create Template", "📊 Template Analytics"])
    
    with tab1:
        st.subheader("Available Process Templates")
        
        # Display process templates from session state
        if st.session_state.process_templates:
            for template_name, template_data in st.session_state.process_templates.items():
                with st.expander(f"📄 {template_name} (Active)"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Steps", len(template_data['steps']))
                    with col2:
                        total_checklist_items = sum(len(step.get('checklist', [])) for step in template_data['steps'])
                        st.metric("Total Checklist Items", total_checklist_items)
                    with col3:
                        avg_sla = sum(step.get('sla_days', step.get('sla', 3)) for step in template_data['steps']) / len(template_data['steps'])
                        st.metric("Avg SLA (days)", f"{avg_sla:.1f}")
                    
                    # Show template description
                    if template_data.get('description'):
                        st.write(f"**Description:** {template_data['description']}")
                    
                    # Show steps with checklists
                    st.write("**Process Flow:**")
                    for i, step in enumerate(template_data['steps'], 1):
                        step_name = step.get('name', f"Step {i}")
                        step_role = step.get('role', 'N/A')
                        step_sla = step.get('sla_days', step.get('sla', 3))
                        
                        st.write(f"**{i}. {step_name}** (Assigned to: {step_role}, SLA: {step_sla} days)")
                        
                        # Show checklist items
                        checklist = step.get('checklist', [])
                        if checklist:
                            st.write("   **Checklist Items:**")
                            for item in checklist:
                                required_icon = "🔴" if item.get('required', True) else "🔵"
                                st.write(f"   {required_icon} {item['name']}")
                                if item.get('description'):
                                    st.write(f"      _{item['description']}_")
                        else:
                            st.write("   _No checklist items defined_")
                    
                    action_cols = st.columns(2)
                    with action_cols[0]:
                        if st.button(f"Edit {template_name}", key=f"edit_{template_name}"):
                            st.info("Template editing interface would open here")
                    with action_cols[1]:
                        if st.button(f"Duplicate {template_name}", key=f"duplicate_{template_name}"):
                            st.info("Template duplication feature would create a copy")
        
        # Display default/legacy templates
        legacy_templates = [
            {"name": "HR Onboarding", "steps": 4, "avg_duration": "5 days", "usage": 12, "status": "Draft", "checklist_items": 8},
            {"name": "Budget Approval", "steps": 3, "avg_duration": "3 days", "usage": 67, "status": "Active", "checklist_items": 5}
        ]
        
        for template in legacy_templates:
            with st.expander(f"📄 {template['name']} ({template['status']})"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Steps", template['steps'])
                with col2:
                    st.metric("Avg Duration", template['avg_duration'])
                with col3:
                    st.metric("Monthly Usage", template['usage'])
                with col4:
                    st.metric("Checklist Items", template['checklist_items'])
                
                if st.button(f"Edit {template['name']}", key=f"edit_{template['name']}"):
                    st.info("Template editing interface would open here")
    
    with tab2:
        st.subheader("Create New Process Template")
        
        with st.form("new_template"):
            template_name = st.text_input("Template Name")
            template_desc = st.text_area("Description")
            
            st.write("**Define Process Steps:**")
            num_steps = st.number_input("Number of Steps", min_value=1, max_value=10, value=3)
            
            # Initialize steps in session state for dynamic management
            if f"template_steps_{template_name}" not in st.session_state:
                st.session_state[f"template_steps_{template_name}"] = []
            
            steps = []
            for i in range(num_steps):
                st.write(f"---")
                st.write(f"**Step {i+1}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    step_name = st.text_input(f"Step {i+1} Name", key=f"step_name_{i}")
                with col2:
                    step_role = st.selectbox(f"Assigned Role", ["PMO", "Manager", "Technical Lead", "Business User"], key=f"step_role_{i}")
                with col3:
                    step_sla = st.number_input(f"SLA (days)", min_value=1, max_value=30, value=3, key=f"step_sla_{i}")
                
                if step_name:
                    step_data = {"name": step_name, "role": step_role, "sla": step_sla, "checklist": []}
                    
                    # Checklist Items Section
                    st.write(f"**📋 Checklist Items for {step_name}**")
                    
                    # Initialize checklist in session state
                    checklist_key = f"checklist_{template_name}_{i}"
                    if checklist_key not in st.session_state:
                        st.session_state[checklist_key] = []
                    
                    # Display existing checklist items
                    for j, item in enumerate(st.session_state[checklist_key]):
                        item_container = st.container()
                        with item_container:
                            item_cols = st.columns([3, 2, 1, 1, 1])
                            
                            with item_cols[0]:
                                item['name'] = st.text_input(f"Item Name", value=item.get('name', ''), key=f"item_name_{i}_{j}")
                            
                            with item_cols[1]:
                                item['description'] = st.text_input(f"Description", value=item.get('description', ''), key=f"item_desc_{i}_{j}")
                            
                            with item_cols[2]:
                                item['required'] = st.checkbox("Required", value=item.get('required', True), key=f"item_req_{i}_{j}")
                            
                            with item_cols[3]:
                                if st.button("↑", key=f"move_up_{i}_{j}", help="Move Up", disabled=(j == 0)):
                                    if j > 0:
                                        st.session_state[checklist_key][j], st.session_state[checklist_key][j-1] = st.session_state[checklist_key][j-1], st.session_state[checklist_key][j]
                                        st.rerun()
                                
                                if st.button("↓", key=f"move_down_{i}_{j}", help="Move Down", disabled=(j == len(st.session_state[checklist_key]) - 1)):
                                    if j < len(st.session_state[checklist_key]) - 1:
                                        st.session_state[checklist_key][j], st.session_state[checklist_key][j+1] = st.session_state[checklist_key][j+1], st.session_state[checklist_key][j]
                                        st.rerun()
                            
                            with item_cols[4]:
                                if st.button("🗑️", key=f"delete_item_{i}_{j}", help="Delete Item"):
                                    st.session_state[checklist_key].pop(j)
                                    st.rerun()
                    
                    # Add new checklist item section
                    with st.expander(f"➕ Add Checklist Item to {step_name}", expanded=False):
                        new_item_cols = st.columns([3, 2, 1, 1])
                        
                        with new_item_cols[0]:
                            new_item_name = st.text_input("New Item Name", key=f"new_item_name_{i}")
                        
                        with new_item_cols[1]:
                            new_item_desc = st.text_input("Description (Optional)", key=f"new_item_desc_{i}")
                        
                        with new_item_cols[2]:
                            new_item_required = st.checkbox("Required", value=True, key=f"new_item_req_{i}")
                        
                        with new_item_cols[3]:
                            if st.button("Add Item", key=f"add_item_{i}"):
                                if new_item_name:
                                    new_item = {
                                        'name': new_item_name,
                                        'description': new_item_desc,
                                        'required': new_item_required
                                    }
                                    st.session_state[checklist_key].append(new_item)
                                    st.rerun()
                                else:
                                    st.error("Item name is required")
                    
                    # Add checklist to step data
                    step_data["checklist"] = st.session_state[checklist_key].copy()
                    steps.append(step_data)
            
            if st.form_submit_button("Create Template"):
                if template_name and len(steps) > 0:
                    # Save template to session state
                    st.session_state.process_templates[template_name] = {
                        'description': template_desc,
                        'steps': steps
                    }
                    
                    # Clear temporary session state
                    for i in range(num_steps):
                        checklist_key = f"checklist_{template_name}_{i}"
                        if checklist_key in st.session_state:
                            del st.session_state[checklist_key]
                    
                    st.success(f"✅ Template '{template_name}' created successfully with {len(steps)} steps!")
                    
                    # Show summary
                    st.subheader("Template Summary")
                    for step in steps:
                        st.write(f"**{step['name']}** ({step['role']}) - {step['sla']} days SLA")
                        if step['checklist']:
                            for item in step['checklist']:
                                required_icon = "🔴" if item['required'] else "🔵"
                                st.write(f"  {required_icon} {item['name']}")
                                if item['description']:
                                    st.write(f"    _{item['description']}_")
                        else:
                            st.write("  _No checklist items defined_")
                else:
                    st.error("Please provide template name and at least one step")
    
    with tab3:
        st.subheader("Template Performance Analytics")
        
        # Template usage chart with checklist data
        template_data = pd.DataFrame({
            'Template': ['IT Project', 'Procurement', 'HR Onboarding', 'Budget Approval'],
            'Usage': [45, 23, 12, 67],
            'Avg Completion Time': [12, 8, 5, 3],
            'Success Rate': [85, 92, 98, 78],
            'Checklist Items': [12, 8, 8, 5],
            'Checklist Compliance': [94, 87, 99, 95]
        })
        
        col1, col2 = st.columns(2)
        with col1:
            fig_usage = px.bar(template_data, x='Template', y='Usage', title="Template Usage (Monthly)")
            st.plotly_chart(fig_usage, use_container_width=True)
        
        with col2:
            fig_success = px.bar(template_data, x='Template', y='Success Rate', title="Template Success Rate (%)")
            st.plotly_chart(fig_success, use_container_width=True)
        
        # Checklist Analytics
        st.subheader("📋 Checklist Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            fig_checklist = px.bar(template_data, x='Template', y='Checklist Items', 
                                 title="Checklist Items per Template")
            st.plotly_chart(fig_checklist, use_container_width=True)
        
        with col2:
            fig_compliance = px.bar(template_data, x='Template', y='Checklist Compliance',
                                  title="Checklist Compliance Rate (%)")
            fig_compliance.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="Target: 90%")
            st.plotly_chart(fig_compliance, use_container_width=True)
        
        # Checklist completion insights
        st.subheader("🎯 Checklist Insights")
        
        insights_data = [
            {"Metric": "Most Skipped Items", "Value": "Optional documentation reviews", "Impact": "Low"},
            {"Metric": "Longest Completion Time", "Value": "Technical feasibility analysis", "Impact": "High"},
            {"Metric": "Highest Failure Rate", "Value": "Budget approval documentation", "Impact": "Medium"},
            {"Metric": "Best Compliance Step", "Value": "Stakeholder identification", "Impact": "Positive"}
        ]
        
        insights_df = pd.DataFrame(insights_data)
        st.dataframe(insights_df, use_container_width=True)
        
        # Template optimization recommendations
        st.subheader("🔧 Optimization Recommendations")
        st.write("1. **Reduce checklist items** in Procurement template - currently has highest item count vs. usage ratio")
        st.write("2. **Add validation steps** to Budget Approval - lowest compliance rate detected")  
        st.write("3. **Consider parallel reviews** for IT Project template - longest average completion time")
        st.write("4. **Standardize descriptions** - 15% of checklist items lack clear descriptions")

elif page == "👤 User Management":
    st.header("User & Role Management")
    
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
                with col1
