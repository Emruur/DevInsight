
# Research and Competitor Analysis

## Github Insights
- ### Contributors
    - Number of comments
    - Number of lines added & deleted
    - Number of pull requests opened & closed (Not implemented in insights)

- ### Code Ceview Collabortion
    - efficiency of code review process
        - !NOT dev specific
            - can be made dev specific by looking at the dominant contributors to the latest pull request
    - Number of reviews per request
        - devs who engage in more reviews?
    - Time taken to perform reviews & number of reviews addresed
        - maybe fast acting devs are better?

    - !! On the other hand, if you observe a developer consistently receiving positive feedback on their code reviews, you can take this as an opportunity to acknowledge their expertise and potentially involve them in mentoring or training activities.
        - sentimental analysis on code reviews 

- ### Issue 
    - Time to resolve issues
    -  ⭐️⭐️⭐️  distrbution of issue resolution times accross people     

- ### Pull Request Performance
    - time it takes to merge pull requests
    - who merges issues? Might be a leader sign?




## CHAOSS Evolution Working Group

The goal of the Evolution working group is to develop metrics to assess the lifecycle of the open source projects.

### Important metrics
- ### Issue Related
    Identify how effective the community is at addressing issues identified by community participants.

    - Issues New	What are the number of new issues created during a certain period?
    - Issues Active	What is the count of issues that showed activity during a certain period?
    - Issues Closed	What is the count of issues that were closed during a certain period?
    - Issue Age	How long have open issues been left open?
    - Issue Response Time	How much time passes between the opening of an issue and a response - in the issue thread from another contributor?
    - Issue Resolution Duration	How long does it take for an issue to be closed?

    ![p](issuemetrics.png)

    - *We might do a personalized issue analysis, how eager to response to issues, how fast the issue is resolved by the developer.*





## What we can add?
- Bus factor calculation and identifying the key developers
    - We can do a bus factor calculation and identfy the busses, and tag them in the dashboard

     - Mívian Ferreira, Thaís Mombach, Marco Tulio Valente, and Kecia Ferreira. 2019.
Algorithms for estimating truck factors: a comparative study. Software Quality
Journal 27, 4 (2019), 1583–1617.

- Developer artifact knowledge measurement
    If we can better understand which devs are knowledgable where, we can better catetorize and analyze them

    - Bella, Sillitti and Succi [11] classified OSS contributors as core, active, occasional and rare developers.
        - Enrico Di Bella, Alberto Sillitti, and Giancarlo Succi. 2013. A multivariate classi- fication of open source developers. Information Sciences 221 (2013), 72–83.

    - Cosentino et al. [9] measured developers’ knowledge on artifacts (e.g. files, directories and project itself) with different metrics such as "last change takes it all" and "multiple changes equally considered".
        - ValerioCosentino,JavierLuisCánovasIzquierdo,andJordiCabot.2015.Assessing the bus factor of Git repositories. In 2015 IEEE 22nd International Conference on Software Analysis, Evolution, and Reengineering (SANER). IEEE, 499–503.

    - Cheng and Guo [8] made an activity-based analysis of OSS contributors, then adopted a data-driven approach to find out the dynamics and roles of the contributors.
        - Jinghui Cheng and Jin LC Guo. 2019. Activity-based analysis of open source software contributors: roles and dynamics. In 2019 IEEE/ACM 12th International Workshop on Cooperative and Human Aspects of Software Engineering (CHASE). IEEE, 11–18.

    - Source File Authorship
        - Thomas Fritz, Gail C Murphy, Emerson Murphy-Hill, Jingwen Ou, and Emily
        Hill. 2014. Degree-of-knowledge: Modeling a developer’s knowledge of code. ACM Transactions on Software Engineering and Methodology (TOSEM) 23, 2 (2014), 1–42.

Eray Hoca Paper
    - In our study, we define reachability similar to this definition. If a developer can reach a file, s/he knows that file. Also, multiple developers can reach the same file at the same time. In the following, we explain how we find reachable files and file coverage for each developer.
          - We define reachable files of a de- veloper as the files that are reached by the developer through the connections in the artifact traceability graph. 

    

    
