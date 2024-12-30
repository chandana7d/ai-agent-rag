
from translator import QueryTranslator
from router import QueryRouter
from retriever import QueryRetriever
from generator import QueryGenerator 
from indexer import ChromaVectorStore
# from crawler import GitHubCrawler
# from indexer import DocumentIndexer

DUPLOCLOUD_QUESTIONS  = [
    "What is the primary capability of the DuploCloud platform?",
    "How does DuploCloud's abstraction differ from traditional PaaS solutions like Heroku?",
    "What are some examples of cloud services that users can directly operate on with DuploCloud?",
    "Which security concepts are typically hidden from end users in DuploCloud?",
    "How does DuploCloud handle direct changes made by administrators on the cloud account?",
    "What is the most fundamental construct in DuploCloud?",
    "How does a Tenant relate to infrastructure in DuploCloud?",
    "What are the four fundamental aspects of a Tenant in DuploCloud?",
    "How does DuploCloud implement security boundaries between Tenants?",
    "How does DuploCloud facilitate user access control at the Tenant level?",
    "How does DuploCloud support billing segregation?",
    "What is a common use case for Tenants in an organization using DuploCloud?",
    "What are the two preexisting Tenants in DuploCloud?",
    "What is the purpose of the Default Tenant in DuploCloud?",
    "How does the Compliance Tenant differ from other Tenants?",
    "How can users configure settings to apply to all new Tenants under a Plan?",
    "Where in the DuploCloud portal can you add Tenant Config settings?",
    "What is the significance of the 'TenantConfig' Config Type?",
    "How can users verify that Tenant Config settings are enabled for new Tenants?",
    "What is the relationship between Plans and Tenant Config settings?",
    "Can Tenant Config settings be applied retroactively to existing Tenants?",
    "How does DuploCloud handle inter-tenant communication?",
    "What role do Security Groups play in Tenant isolation?",
    "How does DuploCloud leverage cloud-specific concepts like IAM roles and Managed Identities?",
    "What is the significance of KMS keys in DuploCloud's Tenant model?",
    "How does DuploCloud handle resource termination when a Tenant is deleted?",
    "Can users have access to multiple Tenants, and how is this managed?",
    "How does DuploCloud's Tenant model support different environments like Dev, QA, and Prod?",
    "What is the purpose of tagging resources with the Tenant's name in the cloud provider?",
    "How does DuploCloud's abstraction model benefit developers without DevOps expertise?"
]


NON_DOC_DUPLOCLOUD_QUESTIONS = [
    "What are DuploCloud's main competitors in the DevOps automation market?",
    "How does DuploCloud's pricing model compare to other DevOps platforms?", 
    "What is the total funding raised by DuploCloud to date?",
    "Who are the founders of DuploCloud and what is their background?",
    "What specific industries or sectors does DuploCloud primarily serve?",
    "How many employees does DuploCloud currently have?",
    "What partnerships or integrations does DuploCloud have with other tech companies?",
    "What is DuploCloud's market share in the DevOps automation industry?",
    "Has DuploCloud won any industry awards or recognitions?",
    "What is the customer retention rate for DuploCloud's services?"
]


def run_pipeline(query):
    vector_store = ChromaVectorStore().get_vectorstore()

    user_query        = QueryTranslator().invoke(query=query)

    r_decision        = QueryRouter(vector_store=vector_store).invoke(query=user_query)
    context           = QueryRetriever().invoke(router_decision=r_decision)
    user_output       = QueryGenerator().invoke(context=context)

    return r_decision, context, user_output

for query in DUPLOCLOUD_QUESTIONS:
    print("------------------------------------------------------------------------------------------")
    print(">>> User Question : ", query)
    r_decision, context, user_output = run_pipeline(query=query)
    #print(">>> ", r_decision.is_vectordb, r_decision.tool_name , len(context.docs) if context.docs is not None else 0  )
    print(f">>> {user_output.content}")

#TEST_QUERY = ["What is the customer retention rate for DuploCloud's services?"]

# for query in NON_DOC_DUPLOCLOUD_QUESTIONS:

#     print("------------------------------------------------------------------------------------------")
#     print(">>> User Question : ", query)
#     r_decision, context, user_output = run_pipeline(query=query)
#     #print(">>> ", r_decision.is_vectordb, r_decision.tool_name , len(context.docs) if context.docs is not None else 0  )
#     print(f">>> {user_output.content}")


# TEMP_QUESTION = ["what is the weather in Seattle?","what is the weather in New York?","what is the weather in SF"]

# for query in TEMP_QUESTION:

#     print("------------------------------------------------------------------------------------------")
#     print(">>> User Question : ", query)
#     r_decision, context, user_output = run_pipeline(query=query)
#     print(">>> ", r_decision.is_vectordb, r_decision.tool_name , len(context.docs) if context.docs is not None else 0  )
#     print(f">>> {user_output.content}")





