# Assemble Decision Perspectives

Here is the decision that needs to be examined:

<decision>
{{DECISION}}
</decision>

Your task is to recommend a set of relevant, opposing perspectives from which
to examine this decision. For example, if one perspective is a early-stage VC,
then the opposing perspective should be a bootstrap entreprenuer with a
lifestyle business.  If one perspective is a mental health and wellbeing
specialist, then the opposing perspective should be from personal growth and
mental resilience specialist.  This is crucial for exploring alternatives and
gathering necessary information to weigh options effectively.

Before providing your final recommendations, please conduct a thorough analysis
of the situation. Wrap your analysis inside <analysis> tags:

<analysis>
1. List the key decision points identified in the situation.
2. Identify all relevant stakeholders who might be affected by or have input on the decision.
3. Outline potential impacts of the decision on various aspects of the business
(e.g., product development, market positioning, financial implications,
customer acquisition).
4. Brainstorm at least 20 initial ideas for different angles that could provide valuable insights:
   a. For each angle, write a brief description and note its uniqueness
   b. Consider the opposing perspectives
5. Evaluate the diversity of your initial ideas:
   a. Are there any major gaps or overlooked areas?
   b. Do the angles cover a range of short-term and long-term considerations?
6. Consider potential biases or blind spots in your initial list of angles.
</analysis>


From these initial list, select 7 angles that will provide the highest
impact and a comprehensive view of the situation. For each selected
perspective, draft:
   - A unique number, like 1, 2, 3, ... that indicates the order of importance. Smaller means higher impact.
   - An explanation of its relevance to the decision
   - A clear title describing who the opposing perspectives are
   - Three specific questions you would ask this pair of conflicting perspective
   - For each question, explain how the answer would impact the decision-making process

Present your final recommendations using the following structure:

<angles>
  <angle>
    <perspectiveA>[A brief, clear description of the perspective, including the domain of expertise or stakeholder group it represents]</perspectiveA>
    <perspectiveB>[The opposing perspective from the above. ]</perspectiveB>
    <relevance>[A concise explanation of why this perspective is important for the decision at hand]</relevance>
    <questions>
      <question>
        [A specific question you would ask an expert from this perspective. Explanation of how the answer to this question could impact the decision. 
      </question>
    </questions>
  </perspective>
  [Repeat the <perspective> structure for each of the perspectives you've identified]
</perspectives>

Remember:

- Make sure you always include 7 different angles.
- Ensure that each perspective is clearly defined and distinct from the others.
- Provide exactly 3 questions for each perspective.
- For every question, include a clear explanation of how the answer will impact the decision-making process.
- The goal is to identify perspectives that will provide a comprehensive understanding of the situation, potential consequences, and alternative approaches that may not have been initially considered.

DO NOT output the analysis.
DO respond with the <angles></angles>.

Please proceed with your analysis and recommendations.
