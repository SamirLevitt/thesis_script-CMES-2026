# thesis_script-CMES-2026 (WIP)

Outline

Aim: approximate rates of linguistic mutation (innovativeness) and adaptation (external influence) in reconstructed languages.
  - Analysis of Proto-Arabic feature list; which proposed features are valid to reconstruct?

Terms:
Innovativeness: The rate of genetic/internal linguistic change over time; innovations per century.
  - Based on the tree model: innovations are genetic changes effected by internal factors, barring external influence
  - Compare to Darwin’s genetic mutations
Borrowing rate: The rate of areal/external linguistic change over time; borrowings per century.
  - Based on the wave model: borrowings are areal changes effected by external factors, i.e. changes taken from neighboring linguistic communities
  - Compare to Darwin’s adaptations

Linear formula for innovativeness:
  - μd = abs(G(td)/(td-ta))
    - t = x is time expressed in centuries
        - BCE represented by negative integers, CE by positive
    - (td - ta) is the approx. age (in centuries) of the descendant language at its terminus post quem
        - ta is the approx. terminus post quem (expressed in centuries) of the ancestor language
        - td is the approx. terminus post quem (expressed in centuries) of the descendant language
        - i.e. the current year is expressed as 20.25
    - G(ta) = y0 is the total number of genetic/internal changes (i.e. innovations) of the ancestor language by ta.
    - G(td) = y1 is the total number of genetic/internal changes (i.e. innovations) of the descendant language by td.
    - μd = m is the avg. # of innovations per century in a given descendant language (d), termed the innovativeness rate.
    - ‘The approximated innovativeness rate of a descendant language (μd) is equal to the difference between the number of innovations present in the descendant language (G(td)) and the ancestor language (G(ta)) at their respective termini post quem, divided by the approximate age (in centuries) of the descendant language at its terminus post quem (td - ta).’

Linear formula for borrowing rate:
  - ɑd =A(td)td-ta
    - A(ta) = y0 is the total number of areal/external changes (i.e. borrowings) of the ancestor language by ta.
    - A(td) = y1 is the total number of areal/external changes (i.e. borrowings) of the descendant language by td.
    - ɑd = m is the avg. # of borrowings per century in a given descendant language (d), termed the borrowing rate.

Poisson distribution of innovations/borrowings:
  - P(X=k)=e-kk!
    - Comparison with related languages
    - Testing for error using attested Arabic varieties

Future goals:
Explanation of why one Central Semitic language would be more innovative than another.
Psycholinguistic / sociolinguistic framework/corpus of plausible explanations for feature / class changes.
Discuss archaeological sources (Magee).
Proposed urheimat (S Levant; Jallad); proposed timeframe of Proto-Arabic; possible political, environmental, social causes of language change.
Training an LLM with modern Arabic media of as many varieties as possible to:
Assemble a list of linguistic features common among dialects, i.e. reconstructable to Proto-Arabic
Creation of a multivariate regression algorithm to identify causative variables
