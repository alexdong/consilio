The detailed situation, including goals, context, options, and considerations have been provided. 


<decision>
{{DECISION}}
</decision>

Your task is to analyze this information thoroughly and formulate insightful
questions. Please follow these steps:

1. Carefully read and understand the situation, paying close attention to all
   provided details.

2. Note down the information you have received:
   - Break down the key elements of the situation
   - Identify potential risks, opportunities, and assumptions in the plan
   - Evaluate short-term and long-term implications of the decision
   - Wrap your analysis process inside <observations></observations> tags.  
    
    <observations>
        <observation>[summary of the observation]</observation>
        [More observations]
    </observations>
 
3. Brainstorm 7-10 questions that explores and clarify information that is
critical to the decision but is absent in the <situation></situation>.
Prioritize areas where your questions could have the most significant impact
that accomplish one or more of the following:

   - Point out potential oversights or gaps in the current plan or proposal
   - Suggest alternative approaches or solutions
   - Stress test the thoroughness of the preparation and planning
   - Open up discussion on specific aspects you find particularly important

For each question, provide a clear and concise explanation, including the
context and rationale behind asking it.

    <questions>
        <question>[Describe what information you are seeking. Detail description on how the response could impact the decision?]</question>
        [More questions]
    </questions>


Remember, your goal at this step is not to provide answers, but to gain a
comprehensive understanding of the context. 

Provide deep, insightful clarification questions that challenge assumptions and
explore potential issues the founder may not have considered. Prioritize depth
and potential impact over surface-level inquiries.

Please produce your response to conform to the following schema:

```md
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <!-- Define the root element -->
    <xs:element name="observe">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="observations" type="observationsType"/>
                <xs:element name="questions" type="questionsType"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    
    <!-- Define the observations section -->
    <xs:complexType name="observationsType">
        <xs:sequence>
            <xs:element name="observation" type="xs:string" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    
    <!-- Define the questions section -->
    <xs:complexType name="questionsType">
        <xs:sequence>
            <xs:element name="question" type="xs:string" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:schema>
```

Please proceed with your observations.
