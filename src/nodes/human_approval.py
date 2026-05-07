from state import SupplyChainState
from db_service import log_decision


def human_approval_node(state: SupplyChainState) -> dict:
    """
    Simulated human approval node - NO LLM.
    
    In production, this would:
    - Send notification to human operator (email, Slack, dashboard alert)
    - Pause workflow and wait for human response
    - Accept approval/rejection/modification input
    
    For MVP, we simulate automatic approval after logging the request.
    
    Args:
        state: Current graph state with final_decision
        
    Returns:
        Partial state update with human_feedback
    """
    final_decision = state.get('final_decision', {})
    decision_type = final_decision.get('decision_type', 'HOLD')
    details = final_decision.get('details', {})
    explanation = final_decision.get('explanation', '')
    decision_risk = state.get('decision_risk', 'UNKNOWN')
    
    # Extract decision details for logging
    supplier_id = details.get('supplier_id')
    quantity = details.get('quantity', 0)
    expedite = details.get('expedite', False)
    
    # Build approval request message
    approval_request = (
        f"HIGH RISK DECISION REQUIRES APPROVAL:\n"
        f"Decision: {decision_type}\n"
        f"Supplier ID: {supplier_id}\n"
        f"Quantity: {quantity} units\n"
        f"Expedite: {expedite}\n"
        f"Risk Level: {decision_risk}\n"
        f"Explanation: {explanation}"
    )
    
    # Log the approval request to database
    approval_log_id = log_decision(
        agent_name='system',
        decision='HUMAN_APPROVAL_REQUESTED',
        reasoning=approval_request
    ) 
    
    # MVP SIMULATION: Auto-approve for testing
    simulated_feedback = "APPROVED"
    
    print("\n" + "="*60)
    print("HUMAN APPROVAL REQUIRED")
    print("="*60)
    print(approval_request)
    print("="*60)
    print(f"SIMULATED RESPONSE: {simulated_feedback}")
    print("="*60 + "\n")
    
    return {
        'human_feedback': simulated_feedback
    }


def post_approval_routing(state: SupplyChainState) -> str:
    """
    Conditional edge function for routing after human approval.
    
    Routes to:
    - "execute" if APPROVED
    - "end" if REJECTED or TIMEOUT_REJECTED
    
    Returns:
        Next node name as string
    """
    human_feedback = state.get('human_feedback', '')
    
    if human_feedback == 'APPROVED':
        return "execute"
    else:
        return "end"
