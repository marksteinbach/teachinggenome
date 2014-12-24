# encoding=utf8

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('text_generation', 'templates'))
template = env.get_template('report_template.html')

import csv
import sys
import os
ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')
from operator import itemgetter
from pychart import *
from xhtml2pdf import pisa
import cStringIO
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

pisa.showLogging()

reload(sys)
sys.setdefaultencoding('utf-8')
	
theme.default_font_size = 14
theme.use_color = True
theme.get_options()
theme.reinitialize()


stock_text = {
	'TOL1': '''-Students are cognitively and emotionally engaged by a rich topic with real-world importance.\n-Students get outside the walls of the classroom.\n-Students see a connection to their own lives and communities.\n-Students experience a sense of discovery.\n-Students reflect on their own learning process.\n-Students feel supported by their teachers, parents and mentors in the community.''',
	'TOL2': '''-Students have freedom (choice, pace, time) within structure (materials, procedures, interaction with materials)\n-Students are completely engaged in a task.\n-Students develop curiosity grounded in knowledge.\n-Students are engaged in a prepared environment and allowed to act on their intrinsic nature to learn.''',
	'TOL3': '''-Students experience collective pressure and support to meet behavioral and academic norms and expectations.\n -Students feel a sense of ongoing accomplishment for meeting commonly recognized benchmarks of mastery.\n-Students experience a highly consistent daily structure for how learning happens.\n-Students are in a highly structured environment with high behavioral expectations and consistent personal consequences for misbehaviors.\n-Students learn content that has been broken down into discrete pieces that are meant to be mastered in sequence and spiraled back to repeatedly until mastery has been achieved.\n-Students get many "at bats" to practice mastering content.\n-They get frequent and consistent feedback on mastery against absolute benchmarks.\n-Students feel a sense of urgency.''',
	'TOL4': '''-Students collaborate explore answers to a complex question.\n-Students operate as a team to uncover the meaning of text or material.\n-Students exercise control (with reasonable limits and accountability) over the direction of a discussion.\n-Students ask difficult questions of each other.\n-Students subsume their own egos and self in favor of deeper understanding of the material, prioritizing self-monitoring of the discussion rather than trying to look smart.\n-Students make their own meaning and meeting their personal learning objectives.''',
	'P1' :  '''-Students learn so that they can develop the experience, character, and skills necessary to make real world decisions that enhance themselves and the communities around them. Students should develop resiliency, perseverance and the ability to understand and follow their interests and passions.''',
	'P2' :  '''-Students learn so that they can be peaceful, mindful, independent citizens who can bring humanity into harmony with the natural order.\n-If we create the right conditions, children will show us their true potential, their natural peacefulness, and they will teach us.''',
	'P3' :  '''-Students learn so that they can go to and through college and thereby change their economic trajectory because going to college is the only way to be successful in society. College provides an opportunity for economic attainment that provides life choices that mirror the freedoms available to middle and high income Americans. ''',
	'P4' :  '''-Students learn so that they can practice and become better at learning.\n-Develop self-reflection and self-discipline with regards to your contributions to the learning community.\n-They can become adept at collective discovery of new learning.''',
	'CI1' : '''-Students should learn a rigorous college-preparatory curriculum that is rooted in real-world experiences. Through structured learning experiences, students learn not only content but also focus their attention on character building and creating high quality products.''',
	'CI2' : '''-Students should learn numeracy, literacy, science, practical life, culture.\n-Curriculum broadly moves from: self and immediate surroundings to self and people around me to self within broader world, so that students learn to take control over their own learning by paying close attention to the world around them and so that they learn to foster a sense of mindfulness.''',
	'CI3' :  '''-Students should learn the skills necessary to get into and succeed in college with an emphasis on academic writing that will give them personal, political and economic empowerment through accessing the power culture. College preparedness is thought of both in terms of academic content and also non-cog skills. The most emphasized non-cognitive skills are persistence and discipline and resiliency.''',
	'CI4' : '''-Students should learn texts that are richly engaging and that represent highly rigorous content.\n-Has historically been done more with humanities, but can be applied to other subjects.\n-Teachers and departments choose texts, which form the basis of curriculum. The exact texts are not as important as the skills they allow the students to practice.''', 
	'CA1' : '''-Students should learn a rigorous college-preparatory curriculum that is rooted in real-world experiences. Through structured learning experiences, students learn not only content but also focus their attention on character building and creating high quality products.''',
	'CA2' : '''-Students should learn numeracy, literacy, science, practical life, culture.\n-Curriculum broadly moves from: self and immediate surroundings to self and people around me to self within broader world, so that students learn to take control over their own learning by paying close attention to the world around them and so that they learn to foster a sense of mindfulness.''',
	'CA3' :  '''-Students should learn the skills necessary to get into and succeed in college with an emphasis on academic writing that will give them personal, political and economic empowerment through accessing the power culture. College preparedness is thought of both in terms of academic content and also non-cog skills. The most emphasized non-cognitive skills are persistence and discipline and resiliency.''',
	'CA4' : '''-Students should learn texts that are richly engaging and that represent highly rigorous content.\n-Has historically been done more with humanities, but can be applied to other subjects.\n-Teachers and departments choose texts, which form the basis of curriculum. The exact texts are not as important as the skills they allow the students to practice.''',
	'LEI1': '''-Physical Setup: Within the classroom, students are usually in groups that are the center of collaboration on project work.\n-Culturally: Students should have a recurring group that serves a non- academic function that supports their learning of process skills related to socio-emotional learning and other non-cognitive skills. This often takes the form of advisories.\n-Procedures and Routines: Instructional routines vary, but there are structures that focus attention and reflection on character traits. Students are encouraged to respect the diverse viewpoints of others and have a safe space to explore their place in the community of the advisory/classroom. Discussions of different types of diversity within the advisory and society are part of the curriculum and seek to create this environment of respect and personal exploration. The advisory-based looping structure allows students intimately know each other and their advisor. Student leadership, inside the advisory, and in the school at large are important ways to build community.\n-Motivation: Student engagement comes from primarily from the selection of topics for the projects and the accountability of group work.''',
	'LEI2': '''-There is heavy control of the environment and the learning material to create calm, focus, respect, curiosity.\n-Physical set up: Design of the classroom is dominated by the idea that the physical environment is the third teacher. There is only one set of each of the learning materials so that students must share and learn how to arbitrate between one another. There should be nothing on the walls (too much stimulus). Very neat and ordered. Wood walls. The room is broken into subjects.\n-Culturally (Mindsets, Expectations): Students learn to respect the learning of other students in the classroom, and take ownership over their own learning.\n-Through Procedures and Routines -Students are free to move about as they please, but there are clear, slow, and mindful routines that children follow: i.e. putting away their mats.\n-Motivation: Students are naturally motivated to learn and the job of the adult is to prepare the environment to do that and then get out of the way.''',
	'LEI3': '''-Physical set up: Rows of tables and chairs with teachers free to circulate around room.\n-Culturally (Mindsets, Expectations): Mindsets are focused on success, respect for rules is paramount, everyone promotes a growth mindset. Through Procedures and Routines: Teacher demands respect from students at all times, and teacher determines the cultural norms of the classroom. Students are held accountable for meeting those expectations. Procedures and routines are practiced  to mastery and deviations from those norms are dealt with swiftly by the teacher. Very small things are dealt with quickly and early so that they do not become bigger issues.\n-Motivation: If the school has adopted this strategy, investment and motivation typically occur at the level of the school, usually with an orientation towards college acceptance. Classroom-level investment messages mirror this school-wide focus.''',
	'LEI4': '''-Physical set up: Students are seated so that no one can 'hide.'\n-Culturally (Mindsets, Expectations): Students respect the opinions of others, and feel free to challenge and build on the comments of others in ways that move the discussion forward. Students have the responsibility for bringing quieter students into the conversation through direct questioning. Through Procedures and Routines: There are several different types discussion formats that a class may cycle through and each one has different protocols that imply different procedures and routines. Focus is NOT on documenting learning, the learning is through the process of discussion.\n-Motivation: The discussion format motivates students to pursue topics of collective interest and to stay engaged in the conversation. The teacher motivates students by selecting texts and writing discussion questions that connect to student interests.''',
	'LEA1': '''-Physical Setup: Within the classroom, students are usually in groups that are the center of collaboration on project work.\n-Culturally: Students should have a recurring group that serves a non-academic function that supports their learning of process skills related to socio-emotional learning and other non-cognitive skills. This often takes the form of advisories.\n-Procedures and Routines: Instructional routines vary, but there are structures that focus attention and reflection on character traits. Students are encouraged to respect the diverse viewpoints of others and have a safe space to explore their place in the community of the advisory/classroom. Discussions of different types of diversity within the  advisory and society are part of the curriculum and seek to create this environment of respect and personal exploration. The advisory-based looping structure allows students intimately know each other and their advisor. Student leadership, inside the advisory, and in the school at large are important ways to build community.\n-Motivation: Student engagement comes from primarily from the selection of topics for the projects and the accountability of group work.''',
	'LEA2': '''-There is heavy control of the environment and the learning material to create calm, focus, respect, curiosity.\n-Physical set up: Design of the classroom is dominated by the idea that the physical environment is the third teacher. There is only one set of each of the learning materials so that students must share and learn how to arbitrate between one another. There should be nothing on the walls (too much stimulus). Very neat and ordered. Wood walls. The room is broken into subjects.\n-Culturally (Mindsets, Expectations): Students learn to respect the learning of other students in the classroom, and take ownership over their own learning.\n-Through Procedures and Routines: Students are free to move about as they please, but there are clear, slow, and mindful routines that children follow: i.e. putting away their mats.\n-Motivation: Students are naturally motivated to learn and the job of the adult is to prepare the environment to do that and then get out of the way.''',
	'LEA3': '''-Physical set up: Rows of tables and chairs with teachers free to circulate around room.\n-Culturally (Mindsets, Expectations): Mindsets are focused on success, respect for rules is paramount, everyone promotes a growth mindset. Through Procedures and Routines: Teacher demands respect from students at all times, and teacher determines the cultural norms of the classroom. Students are held accountable for meeting those expectations. Procedures and routines are practiced to mastery and deviations from those norms are dealt with swiftly by the teacher. Very small things are dealt with quickly and early so that they do not become bigger issues.\n-Motivation: If the school has adopted this strategy, investment and motivation typically occur at the level of the school, usually with an orientation towards college acceptance. Classroom-level investment messages mirror this school-wide focus.''',
	'LEA4': '''-Physical set up: Students are seated so that no one can hide.\n-Culturally (Mindsets, Expectations): Students respect the opinions of others, and feel free to challenge and build on the comments of others in ways that move the discussion forward. Students have the responsibility for bringing quieter students into the conversation through direct questioning. Through Procedures and Routines: There are several different types discussion formats that a class may cycle through and each one has different protocols that imply different procedures and routines. Focus is NOT on documenting learning, the learning is through the process of discussion.\n-Motivation: The discussion format motivates students to pursue topics of collective interest and to stay engaged in the conversation. The teacher motivates students by selecting texts and writing discussion questions that connect to student interests.''',
	'PI1':  '''-Over the year?: The teacher, or team of teachers, plans a series of units, each of which is linked to a capstone experience that puts the work into a real-world context. The planning involves both an arc of content and a skill and character development arc.\n-At the unit level?: Teachers often start with an immersive event in order to build engagement, but may choose to put the real-world experience at the beginning or end of the unit depending on which will serve the pedagogical needs of the unit. Projects form the core learning experiences at the unit level.\n-At the daily level?: Teachers plan how the work on the project will unfold from day to day. ''',
	'PI2':  '''-The planning is done lesson by lesson following the needs of the students.\n-Having the curriculum and the environment ready allows the guide to focus on the children.\n-The fundamentals are delivered in as simple and precise a way as possible so that the teacher can quickly get out of the way and allow the students to take control of the learning.''',
	'PI3':  '''-Over the year? Plans for the yearlong delivery of content are dictated by the sequence most likely to result in mastery beyond the level of state assessments.\n-At the unit level? All teachers generally use the same long-term and unit plans which mirror some elements of UBD, but generally without performance assessments.\n-At the daily level? Daily lesson plans follow backwards planning philosophy with 5 major steps: Do Now, Hook, Introduction to New Material, Guided Practice, Independent Practice and closing. Lesson and unit plans are generally tightly planned down to the level of specific teacher and student actions.''',
	'PI4':  '''-Instructor thinks carefully about the selection of texts and the discussion method that will best meet the objectives. (Bubble Up, General to Particular, Particular to General, Top Down).\n-Over the year? Teachers think about thematic progression over the year so that students are coming to understanding of themes. Additionally, they are thinking much more about skills rather than about specific content.\n-At the unit and daily level? Planning at the unit and daily level is about coming up with questions that challenge, resist easy answers, and highlight the central tensions with the texts. Additionally, these questions need to lead students to deeper understanding about how the material informs their knowledge and conceptions about the world. Teachers in this style do not start with objectives and are not about choreographing experiences for students.''',
	'PA1':  '''-Over the year?: The teacher, or team of teachers, plans a series of units, each of which is linked to a capstone experience that puts the work into a real-world context. The planning involves both an arc of content and a skill and character development arc.\n-At the unit level?: Teachers often start with an immersive event in order to build engagement, but may choose to put the real-world experience at the beginning or end of the unit depending on which will serve the pedagogical needs of the unit. Projects form the core learning experiences at the unit level.\n-At the daily level?: Teachers plan how the work on the project will unfold from day to day. ''',
	'PA2':  '''-The planning is done lesson by lesson following the needs of the students.\n-Having the curriculum and the environment ready allows the guide to focus on the children.\n-The fundamentals are delivered in as simple and precise a way as possible so that the teacher can quickly get out of the way and allow the students to take control of the learning.''',
	'PA3':  '''-Over the year? Plans for the yearlong delivery of content are dictated by the sequence most likely to result in mastery beyond the level of state assessments.\n-At the unit level? All teachers generally use the same long-term and unit plans which mirror some elements of UBD, but generally without performance assessments.\n-At the daily level? Daily lesson plans follow backwards planning philosophy with 5 major steps: Do Now, Hook, Introduction to New Material, Guided Practice, Independent Practice and closing. Lesson and unit plans are generally tightly planned down to the level of specific teacher and student actions.''',
	'PA4':  '''-Instructor thinks carefully about the selection of texts and the discussion method that will best meet the objectives. (Bubble Up, General to Particular, Particular to General, Top Down).\n-Over the year? Teachers think about thematic progression over the year so that students are coming to understanding of themes. Additionally, they are thinking much more about skills rather than about specific content.\n-At the unit and daily level? Planning at the unit and daily level is about coming up with questions that challenge, resist easy answers, and highlight the central tensions with the texts. Additionally, these questions need to lead students to deeper understanding about how the material informs their knowledge and conceptions about the world. Teachers in this style do not start with objectives and are not about choreographing experiences for students.''',
	'EI1':  '''-Teacher plays the role of facilitating learning experiences for the students and structuring the reflection and debriefing opportunities that allow the students to consolidate learning from experiences.\n-Delivering Content- Teacher connect students to authentic experiences that allow students to explore passions and interests.\n-Facilitating Practice: The teacher manages the protocols that students use to make sense of the real-world, authentic experiences that form the core of true learning.\n-Checking for Understanding: Through consultations with students during advising meetings and through observation of the debriefing/meaning making processes.\n-Responding/Adjusting Instruction to Misunderstandings: Often, teachers have to closely observe student meaning-making processes in order to best plan experiences that will address misunderstandings.''',
	'EI2':  '''-The teacher is referred to as guide. He or she acts more as a facilitator and coach/mentor than a typical teacher.\n-Delivering Content: There is a specific way that a teacher should deliver each lesson: 1. Naming the new knowledge, 2. Supporting Recognition and Association, and then 3. Facilitating Recall. The delivery is done by a teacher for one or two children.\n-Facilitating Practice: Guided by students: teacher helps maintain attention and focus.\n-Checking for Understanding: Through individual check ins with students.\n-Responding/Adjusting Instruction to Misunderstandings: If a teacher saw a student struggling with a lesson, the teacher may ask to reteach the lesson later, but probably won't interrupt the learning of the child.''',
	'EI3':  '''-Delivering Content: The role of the teacher is to break down the task into discrete steps which can be modeled to students. The teacher generally presents the steps on the board or projector in a way that can be captured by students in structured notes\n-Facilitating Practice: Each of the steps outlined in the Introduction to New Material are practiced after they are introduced. The role of the teacher is to provide as many at-bat opportunities as possible through clear expectations and tight execution.\n-Checking for Understanding: Multiple checks for understanding throughout the lesson, not just at the end. On the lesson level, techniques like "Cold Call" and other ways of quick gauging student mastery of steps allow for rapid re-direction of misconceptions. Outside of the individual lesson level, there is an emphasis on quantitative data analysis to uncover trends in student learning that will allow for remediation and support.\n-Responding/Adjusting Instruction to Misunderstandings - "right is right" - students are held accountable to articulating the right response, sometime after getting it modeled by another student, or after sufficient interim time to come up with the right response.''',
	'EI4':  '''-Delivering Content: Intervene only when necessary; to correct behavior or redirect discussion. There are rarely times when the teacher should deliver content. Instead, content delivery should primarily come through shared texts. Facilitating Practice: Teacher interjects with different types of questions (open-action, hypothetical, action....) in order to further the discussion. Teacher considers the skills around contributing to discussion. gives feedback about the way in which students.\n-Checking for Understanding: Ensuring students cite textual evidence for claims.\n-Responding/Adjusting Instruction to Misunderstandings: Move the discussion forward and up/down to greater depth.''',
	'EA1':  '''-Teacher plays the role of facilitating learning experiences for the students and structuring the reflection and debriefing opportunities that allow the students to consolidate learning from experiences.\n-Delivering Content- Teacher connect students to authentic experiences that allow students to explore passions and interests.\n-Facilitating Practice: The teacher manages the protocols that students use to make sense of the real-world, authentic experiences that form the core of true learning.\n-Checking for Understanding: Through consultations with students during advising meetings and through observation of the debriefing/meaning making processes.\n-Responding/Adjusting Instruction to Misunderstandings: Often, teachers have to closely observe student meaning-making processes in order to best plan experiences that will address misunderstandings.''',
	'EA2':  '''-The teacher is referred to as "guide.” He or she acts more as a facilitator and coach/mentor than a typical teacher.\n-Delivering Content: There is a specific way that a teacher should deliver each lesson: 1. Naming the new knowledge, 2. Supporting Recognition and Association, and then 3. Facilitating Recall. The delivery is done by a teacher for one or two children.\n-Facilitating Practice: Guided by students - teacher helps maintain attention and focus.\n-Checking for Understanding: Through individual check ins with students.\n-Responding/Adjusting Instruction to Misunderstandings: If a teacher saw a student struggling with a lesson, the teacher may ask to reteach the lesson later, but probably won't interrupt the child's learning.''',
	'EA3':  '''-Delivering Content - Teachers' role is to break down the task into discrete steps which can be modeled to students. The teacher generally presents the steps on the board or projector in a way that can be captured by students in structured notes. \n-Facilitating Practice - Each of the steps outlined in the Introduction to New Material are practiced after they are introduced. The teachers' role is to provide as many "at bat” opportunities as possible through clear expectations and tight execution.\n-Checking for Understanding - Multiple checks for understanding throughout the lesson, not just at the end. On the lesson level, techniques like "Cold Call" and other ways of quick gauging student mastery of steps allow for rapid re-direction of misconceptions. Outside of the individual lesson level, there is an emphasis on quantitative data analysis to uncover trends in student learning that will allow for remediation and support.\n-Responding/Adjusting Instruction to Misunderstandings - "right is right" - students are held accountable to articulating the right response, sometime after getting it modeled by another student, or after sufficient interim time to come up with the right response.''',
	'EA4':  '''-Delivering Content - Intervene only when necessary; to correct behavior or redirect discussion. There are rarely times when the teacher should deliver content. Instead, content delivery should primarily come through shared texts. Facilitating Practice - Teacher interjects with different types of questions (open-action, hypothetical, action....) in order to further the discussion. Teacher considers the skills around contributing to discussion. gives feedback about the way in which students.\n-Checking for Understanding - Ensuring students cite textual evidence for claims.\n-Responding/Adjusting Instruction to Misunderstandings: Move the discussion forward and up/down to greater depth.''',
	'MI1':  '''-Responses are framed in the context of shared and publicly established values.\n-Leverage strong personal relationships with students to prevent most misbehaviors.\n-Create a classroom culture based on mutual accountability and oriented around a collective endeavor.\n-Transgressions are handled by the group. The group should discuss how and why the issue occurred and how it will be avoided in the future.''',
	'MI2':  '''-As much as possible, teachers should refrain from explicit rewards or punishments for behavior. Extrinsic motivation takes the power away from the child and puts the pressure on them to perform for you.\n-Teachers take the time to observe and understand each child's individual needs and what kind of interventions each child will need to move closer to being effectively socialized.\n-The role of the teacher is to give appropriate help to support the child to come back from the deviation from positive behavior. The teacher's role is to find a way to channel the child's energy into something more productive.''',
	'MI3':  '''-Teachers are responsible for holding students to the behavioral expectations uniformly, without exception.\n-Minor disruptions are "nipped in the bud" and sweating the small stuff is seen as a way of preventing larger issues.''',
	'MI4':  '''-Teachers are responsible for cultivating a generosity and openness to ideas among all the members of the classroom community. Because learning is a shared enterprise of the whole community, disruptions are usually addressed based on the action or comment and how it impacts the discussion. More severe behavioral issues may be handled in a private discussion outside of class.''',
	'MA1':  '''-Responses are framed in the context of shared and publicly established values.\n-Leverage strong personal relationships with students to prevent most misbehaviors.\n-Create a classroom culture based on mutual accountability and oriented around a collective endeavor.\n-Transgressions are handled by the group. The group should discuss how and why the issue occurred and how it will be avoided in the future.''',
	'MA2':  '''-As much as possible, teachers should refrain from explicit rewards or punishments for behavior. Extrinsic motivation takes the power away from the child and puts the pressure on them to perform for you.\n-Teachers take the time to observe and understand each child's individual needs and what kind of interventions each child will need to move closer to being effectively socialized.\n-The role of the teacher is to give appropriate help to support the child to come back from the deviation from positive behavior. The teacher's role is to find a way to channel the child's energy into something more productive.''',
	'MA3':  '''-Teachers are responsible for holding students to the behavioral expectations uniformly, without exception.\n-Minor disruptions are "nipped in the bud” and sweating the small stuff is seen as a way of preventing larger issues.''',
	'MA4':  '''-Teachers are responsible for cultivating a generosity and openness to ideas among all the members of the classroom community. Because learning is a shared enterprise of the whole community, disruptions are usually addressed based on the action or comment and how it impacts the discussion. More severe behavioral issues may be handled in a private discussion outside of class.''',
	'AI1':  '''-How often? - Assessments are usually done at the end of a project. Though informal daily assessments of student learning are common.\n-With what instruments?: Much of the assessment is through execution of performance assessments made up of authentic tasks, usually in the form of externally facing product or performance. Common rubrics are typically used across teachers. Community members can also be involved in the assessment process in order to further increase authenticity and real-world applicability.\n-For what purpose?: To determine the student's individual mastery of both content and skills, as well as determine the extent to which the student displayed the character traits selected by the school community. The performative assessment and the application of the rubric by a broad cross-section of the community is also meant to make the connection that learning has real application in the world.''',
	'AI2':  '''-How often? - Assessment is done constantly.\n-With what instruments?: As much as possible, assessment is highly individualized, qualitative, and authentic. It is constant, deep observation, recording, and reflection.\n-The primary measure of student learning is observation, embodying the very essence of "formative assessment”, determining where the student is in their formation and meeting of skill based benchmarks and considering new learning experiences to meet those needs. \n-For what purpose?: Teacher is observing how the students are using the materials, when they have mastered a concept, and when they are ready to move onto the next step.''',
	'AI3':  '''-How often? - Paper and pencil assessments are frequently used to capture mastery, typically weekly. Exit slips are always used to capture objective level mastery at the daily level. Many teachers use weekly quizzes to assess progress towards broader unit level understandings. Unit assessments assess "enduring understandings" and application of material or state standards level mastery, depending on the school.\n-With what instruments?: Most assessments are a mix of multiple choice and open response questions.\n-For what purpose?: Continuous improvement and mastery at every level. Results inform new strategies at both the classroom and school level and responsive teaching. Mastery results are also used to motivate students and staff in ongoing progress. The school results also have important implications in terms of governing board expectations and accountability requirements.''',
	'AI4':  '''-The teachers should determine how he or she will assess student discussion and how this assessment will be reflected in grades. This may sometimes be done in collaboration with students. Writing also features prominently as the ideal instrument for determining student understanding.\n-How often?: Every discussion. Writing assignments or other assessments may be given more periodically to assess unit-level understanding. discussion. Papers and other assessments are given more periodically. \n-With what instruments?: The teacher should create a map of who has talked and how often. The teacher should keep track of dynamics in the classroom during the discussion, for example, who builds upon the comments made by others, and who seems to dominate the discussion without bringing other viewpoints in.\n-For what purpose? Motivating students to participate frequently and with purpose. Motivate student to behave in ways that support the larger discussion. Modeling for students how to reflect on group dynamics.''',
	'AA1':  '''-How often? - Assessments are usually done at the end of a project. Though informal daily assessments of student learning are common.\n-With what instruments?: Much of the assessment is through execution of performance assessments made up of authentic tasks, usually in the form of externally facing product or performance. Common rubrics are typically used across teachers. Community members can also be involved in the assessment process in order to further increase authenticity and real-world applicability. \n-For what purpose?: To determine the student's individual mastery of both content and skills, as well as determine the extent to which the student displayed the character traits selected by the school community. The performative assessment and the application of the rubric by a broad cross-section of the community is also meant to make the connection that learning has real application in the world.''',
	'AA2':  '''-How often? - Assessment is done constantly.\n-With what instruments?: As much as possible, assessment is highly individualized, qualitative, and authentic. It is constant, deep observation, recording, and reflection.\n-The primary measure of student learning is observation, embodying the very essence of "formative assessment”, determining where the student is in their formation and meeting of skill based benchmarks and considering new learning experiences to meet those needs. \n-For what purpose?: Teacher is observing how the students are using the materials, when they have mastered a concept, and when they are ready to move onto the next step.''',
	'AA3':  '''-How often?: Paper and pencil assessments are frequently used to capture mastery, typically weekly. Exit slips are always used to capture objective level mastery at the daily level. Many teachers use weekly quizzes to assess progress towards broader unit level understandings. Unit assessments assess "enduring understandings" and application of material or state standards level mastery, depending on the school.\n-With what instruments?: Most assessments are a mix of multiple choice and open response questions.\n-For what purpose?: Continuous improvement and mastery at every level. Results inform new strategies at both the classroom and school level and responsive teaching. Mastery results are also used to motivate students and staff in ongoing progress. The school results also have important implications in terms of governing board expectations and accountability requirements.''',
	'AA4':  '''-The teachers should determine how he or she will assess student discussion and how this assessment will be reflected in grades. This may sometimes be done in collaboration with students. Writing also features prominently as the ideal instrument for determining student understanding.\n-How often?: Every discussion. Writing assignments or other assessments may be given more periodically to assess unit-level understanding. discussion. Papers and other assessments are given more periodically.\n-With what instruments?: The teacher should create a map of who has talked and how often. The teacher should keep track of dynamics in the classroom during the discussion, for example, who builds upon the comments made by others, and who seems to dominate the discussion without bringing other viewpoints in.\n-For what purpose? Motivating students to participate frequently and with purpose. Motivate student to behave in ways that support the larger discussion. Modeling for students how to reflect on group dynamics.'''                  
} 

style = {'TOL1': 'Theory of Learning: Teaching as project Based Exploration',
		'P1': 'Purpose: Teaching as project Based Exploration',
		'CI1': 'Curriculum (Intent): Teaching as project Based Exploration',
		'CA1': 'Curriculum (Action): Teaching as project Based Exploration',
		'LEI1': 'Learning Environment (Intent): Teaching as project Based Exploration',
		'LEA1': 'Learning Environment (Action): Teaching as project Based Exploration',
		'PI1': 'Planning (Intent): Teaching as project Based Exploration',
		'PA1': 'Planning (Action): Teaching as project Based Exploration',
		'EI1': 'Execution (Intent): Teaching as project Based Exploration',
		'EA1': 'Execution (Action): Teaching as project Based Exploration',
		'MI1': 'Managment (Intent): Teaching as project Based Exploration',
		'MA1': 'Management (Action): Teaching as project Based Exploration',
		'AI1': 'Assessment (Intent): Teaching as project Based Exploration',
		'AA1': 'assessment (Action): Teaching as project Based Exploration',
		'TOL2': 'Theory of Learning: Teaching as Developing Individual Agency',
		'P2': 'Purpose: Teaching as Developing Individual Agency',
		'CI2': 'Curriculum (Intent): Teaching as Developing Individual Agency',
		'CA2': 'Curriculum (Action): Teaching as Developing Individual Agency',
		'LEI2': 'Learning Environment (Intent): Teaching as Developing Individual Agency',
		'LEA2': 'Learning Environment (Action): Teaching as Developing Individual Agency',
		'PI2': 'Planning (Intent): Teaching as Developing Individual Agency',
		'PA2': 'Planning (Action): Teaching as Developing Individual Agency',
		'EI2': 'Execution (Intent): Teaching as Developing Individual Agency',
		'EA2': 'Execution (Action): Teaching as Developing Individual Agency',
		'MI2': 'Management (Intent): Teaching as Developing Individual Agency',
		'MA2': 'Management (Action): Teaching as Developing Individual Agency',
		'AI2': 'Assessment (Intent): Teaching as Developing Individual Agency',
		'AA2': 'Assessment (Action): Teaching as Developing Individual Agency',
		'TOL3': 'Theory of Learning: Teaching as Efficient Coaching',
		'P3': 'Purpose: Teaching as Efficient Coaching',
		'CI3': 'Curriculum (Intent): Teaching as Efficient Coaching',
		'CA3': 'Curriculum (Action): Teaching as Efficient Coaching',
		'LEI3': 'Learning Environment (Intent): Teaching as Efficient Coaching',
		'LEA3': 'Learning Environment (Action): Teaching as Efficient Coaching',
		'PI3': 'Planning (Intent): Teaching as Efficient Coaching',
		'PA3': 'Planning (Action): Teaching as Efficient Coaching',
		'EI3': 'Execution (Intent): Teaching as Efficient Coaching',
		'EA3': 'Execution (Action): Teaching as Efficient Coaching',
		'MI3': 'Management (Intent): Teaching as Efficient Coaching',
		'MA3': 'Management (Action): Teaching as Efficient Coaching',
		'AI3': 'Assessment (Intent): Teaching as Efficient Coaching',
		'AA3': 'Assessment (Action): Teaching as Efficient Coaching',
		'TOL4': 'Theory of Learning: Teaching as Collective Facilitation',
		'P4': 'Purpose: Teaching as Collective Facilitation',
		'CI4': 'Curriculum (Intent): Teaching as Collective Facilitation',
		'CA4': 'Curriculum (Action): Teaching as Collective Facilitation',
		'LEI4': 'Learning Environment (Intent): Teaching as Collective Facilitation',
		'LEA4': 'Learning Environment (Action): Teaching as Collective Facilitation',
		'PI4': 'Planning (Intent): Teaching as Collective Facilitation',
		'PA4': 'Planning (Action): Teaching as Collective Facilitation',
		'EI4': 'Execution (Intent): Teaching as Collective Facilitation',
		'EA4': 'Execution (Action): Teaching as Collective Facilitation',
		'MI4': 'Management (Intent): Teaching as Collective Facilitation',
		'MA4': 'Management (Action): Teaching as Collective Facilitation',
		'AI4': 'Assessment (Intent): Teaching as Collective Facilitation',
		'AA4': 'Assessment (Action): Teaching as Collective Facilitation'
}		

def fix_dim(dim):
    ret = []
    for d in dim:
        sty = style[d[0]].split(':')[-1].strip()
        ret.append(("%s (%s%%)" % (sty, int(d[1])), d[1]))
    return ret

report_order = [13, 10, 3, 2, 7, 6, 12, 11, 5, 4, 9, 8, 1, 0]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

f = open(sys.argv[1],'rU')

dataholder = {}

def fix_text(text):
	lines = text.split('\n')
	return ''.join(["<li>%s</li>" % line.replace("-", "") for line in lines])
	
try:
    reader = csv.DictReader(f)
    for row in reader:
		user_data = {'most_inclined': {}, 'least_inclined': {}}
		int_row = {k:float(v) if is_number(v) == True else v for k,v in row.items()}
		dimension_bank = sorted(int_row.items())
		dimension_list = zip(*([iter(dimension_bank)] * 4))
		username = dimension_list[14][2][1]
		user_email = dimension_list[14][1][1]
		date_taken = dimension_list[14][0][1]
		user_data['email'] = user_email
		user_data['date_taken'] = date_taken
		user_data['name'] = username
		del dimension_list[14]
		sorted_dimension_list = [dimension_list[i] for i in report_order]
		most_inclined_keys = []
		least_inclined_keys = []
		if not os.path.exists(username.replace(" ", "")):
		    os.mkdir(username.replace(" ", ""))		
		
		# create list of keys associated with most and least inclined styles for each dimension
		
		for dimension in sorted_dimension_list:
			most_inclined = max(dimension,key=itemgetter(1))[0]
			least_inclined = min(dimension,key=itemgetter(1))[0]
			most_inclined_keys.append(most_inclined)
			least_inclined_keys.append(least_inclined)
			
		# create a pie chart based on the values and styles in each dimension	
			
			fixed_dim = fix_dim(dimension)
			cnv = canvas.init("%s/graph_%s.png" % (username.replace(" ", ""), most_inclined[:-1]))
			ar = area.T(size=(800,300), legend = None, x_grid_style = None, y_grid_style = None)
			plot = pie_plot.T(data=fixed_dim, arc_offsets=[0,0,0,0], shadow = (2, -2, fill_style.gray50), label_offset = 25, arrow_style = arrow.a0, fill_styles = [fill_style.Plain(bgcolor = color.blue), fill_style.Plain(bgcolor = color.red1), fill_style.Plain(bgcolor = color.yellow), fill_style.Plain(bgcolor = color.springgreen1)])
			ar.add_plot(plot)
			ar.draw()

				
		# attach the appropriate stock text to most and least inclined keys
			
		for i,j in zip(most_inclined_keys, least_inclined_keys):	
			data = []
			most_inclined_text = stock_text[i]
			least_inclined_text = stock_text[j]
			fixed_mit = fix_text(most_inclined_text)
			fixed_lit = fix_text(least_inclined_text)
			user_data['most_inclined'][i[:-1]] = [i, "<ul>%s</ul>" % fixed_mit]
			user_data['least_inclined'][j[:-1]] = [j, "<ul>%s</ul>" % fixed_lit]
		
		# create HTML document based on stock text and graphics
		
		html = template.render(user=user_data, style=style)
		html_out = open('%s/out.html' % username.replace(" ", ""), 'w')
		html_out.write(html)
		
		# send email to user with report attached
		
		msg = MIMEMultipart()
		msg['Subject'] = 'Your Teaching Genome Report'
		msg['From'] = 'info@teachinggenome.com' # get new email
		msg['To'] = 'mark.v.steinbach@gmail.com'
		msg.preamble = 'Your Teaching Genome Report\n'
		part = MIMEText("Email info@teachinggenome.com if you have difficulty viewing this file.")
		msg.attach(part)
		part = MIMEApplication(open(ROOT('%s/out.pdf') % username.replace(" ", ""),'rb').read(), 'pdf', name="MyTeachingGenomeReport.pdf")
		msg.attach(part)
		smtp = SMTP("smtp.gmail.com", 587)
		smtp.ehlo()
		smtp.starttls()
		smtp.login("info@teachinggenome.com", "Teaching is hard.")
		smtp.sendmail(msg['From'], msg['To'], msg.as_string())
finally:
    f.close()	



    
	
