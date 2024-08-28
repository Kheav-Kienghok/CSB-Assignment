import pandas as pd
from urllib.request import urlopen
from io import StringIO


class SchoolAssessmentAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()
        self.summary_data = []

    def process_file(self, file_path):
        # Open and read the content of the file
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.data = pd.read_excel(file_path)
        elif file_path.endswith('.txt'):
            self.data = pd.read_csv(file_path, delimiter='\t')


    def transfer_data(self, criteria, destination_file):
        # Transfer data based on predefined criteria
        try:
            subject_list = ['INF_652', 'CSC_241', 'ITM_101', 'ITM_371', 'COSC_201']
            self.data['Score'] = self.data[subject_list].mean(axis=1)

            filtered_data = self.data.query(criteria)
            filtered_data.to_csv(destination_file, index=False)
            print(f"Filtered data has been saved to {destination_file}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
 
    def fetch_web_data(self, url):
        # Fetch data from school webpage using urlopen
        try:
            with urlopen(url) as response:
            # Custom logic to extract relevant information from the webpage
                content = response.read().decode('utf-8')
                self.data = pd.read_csv(StringIO(content))
        except Exception as e:
            print(f"Error fetching web data: {e}")
            

    def analyze_content(self, student_name):
        # Custom logic to analyze assessment data (e.g., calculate averages, identify trends)
        try:
            subject_list = ['INF_652', 'CSC_241', 'ITM_101', 'ITM_371', 'COSC_201']
            student_data = self.data[self.data['Name'] == student_name]
            if not student_data.empty:
                student_summary = self._generate_student_summary(student_data, subject_list)
                self.summary_data.append(student_summary)
            else:
                print(f"Student '{student_name}' not found in data.")
        except Exception as e:
            print(f"An error occurred during content analysis: {e}")
    
    def determine_grade(self, avg_score):
        if avg_score > 89:
            return 'A'
        elif avg_score > 79:
            return 'B'
        elif avg_score > 69:
            return 'C'
        elif avg_score > 59:
            return 'D'
        elif avg_score > 49:
            return 'F'
        else:
            return 'F'

    def _generate_student_summary(self, student_data, subject_list):
        try:
            semester = student_data['Semester'].iloc[0]
            id = student_data['Id'].iloc[0]
            email = student_data['URL'].iloc[0]
            avg_score = student_data[subject_list].mean(axis=1).mean()
            grade = self.determine_grade(avg_score)
            highest_scoring_subject = student_data[subject_list].idxmax(axis=1).iloc[0]
            highest_score = student_data[highest_scoring_subject].iloc[0]
            lowest_class = student_data[subject_list].mean().idxmin()
            lowest_score = student_data[subject_list].min().min()
            notable_observations = student_data[subject_list].idxmax(axis=1).value_counts().idxmax()
            web_data_time = student_data['Time Spent'].str.extract(r'(\d+)m').astype(int).sum().values[0]
            subject_analysis = self._subject_analysis(student_data, subject_list)

            return {
                'Name': student_data['Name'].iloc[0],
                'id': id,
                'email': email,
                'Semester': semester,
                'Average Score': avg_score,
                'Grade': grade,
                'Highest Score': highest_score,
                'Lowest Score': lowest_score,
                'Lowest Class': lowest_class,
                'Notable Observation': notable_observations,
                'Online Participation': web_data_time,
                'Subject Analysis': subject_analysis
            }
        except Exception as e:
            print(f"An error occurred while generating the student summary: {e}")

    def _subject_analysis(self, student_data, subject_list):
        try:
            subject_grade = []
            for subject in subject_list:
                score = student_data[subject].iloc[0]
                sub_grade = self.determine_grade(score)
                subject_grade.append(f"   - {subject}: Score: {score}, Grade: {sub_grade}")
            return '\n'.join(subject_grade)
        except Exception as e:
            print(f"An error occurred during subject analysis: {e}")


    def generate_summary(self, summary_data):
        # Generate summary for the school principal
        # Include key insights, trends, and areas of improvement
        try:
            if not summary_data:
                return "No student data analyzed yet. Please run analyze_content first."
            summary_report = "\n\nSchool Assessment Summary Report:\n"
            for student in summary_data:
                summary_report += f"====================================\n"
                summary_report += f"Student name: {student['Name']}\n"
                summary_report += f"Student ID: {student['id']}\n"
                summary_report += f"Enroll in: {student['Semester']}\n\n"
                summary_report += f"1. Overall Performance:\n"
                summary_report += f"   - Average score: {student['Average Score']:.1f}\n"
                summary_report += f"   - Overall Grade: {student['Grade']}\n"
                summary_report += f"2. Subject-wise Analysis:\n"
                summary_report += f"   + Subject grades:\n{student['Subject Analysis']}\n"
                summary_report += f"   * {student['Notable Observation']}: Highest scoring subject of {student['Highest Score']}.\n"
                summary_report += f"   * {student['Lowest Class']}: Lowest scoring subject of {student['Lowest Score']}.\n"
                summary_report += f"3. Notable Observations:\n"
                summary_report += f"   - {student['Notable Observation']} course shows a great accomplishment.\n"
                summary_report += f"4. Web Data Insights:\n"
                summary_report += f"   - Student email: {student['email']}\n"
                summary_report += f"   - Online class participation duration: {student['Online Participation']} minutes\n"
                summary_report += f"5. Recommendations:\n"
                summary_report += f"   - Try to improve your performance in {student['Lowest Class']} course.\n\n"
            summary_report += f"Report generated on: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n"
            return summary_report
        except Exception as e:
            print(f"An error occurred while generating the summary: {e}")
            
    def save_summary_to_file(self, summary, filename='text.txt'):
        try:
            with open(filename, 'w') as file:
                file.write(summary)
            print(f"Summary report saved to {filename}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example Usage
analyzer = SchoolAssessmentAnalyzer()

# Process files
analyzer.process_file('all_semester.csv')

# Transfer data
analyzer.transfer_data('Score > 90', 'high_achievers.csv')

# Fetch web data
# analyzer.fetch_web_data(r'https://raw.githubusercontent.com/Kheav-Kienghok/CSB-Assignment/main/web%20log.csv')
analyzer.fetch_web_data(r"https://raw.githubusercontent.com/Kheav-Kienghok/CSB-Assignment/main/all_semester.csv")

# Analyze content
name = input("Enter the student name: ")
analyzer.analyze_content(name)

# Generate summary
summary = analyzer.generate_summary(analyzer.summary_data)
print(summary)
save_file = analyzer.save_summary_to_file(summary, 'assessment_summary_report.txt')