# importing all needed packages and/or libraries
import argparse
import pandas as pd
import random as r
import matplotlib.pyplot as plt
import seaborn as sns


# Class containing all functions
class DataAnalyzer:
    def __init__(self, dataset):
        self.dataset = dataset

    #this function describes the data
    def data_describer(self):
        brief_description = ""
        num_rows, num_cols = self.dataset.shape
        brief_description = f"The dataset contains {num_rows} rows and {num_cols} columns.\n"
        brief_description += "The data types of each column are: \n"
        brief_description += str(self.dataset.dtypes) + "\n"
        return brief_description

    # this is the data cleaning
    def data_cleaner(self):
        # drops duplicates and fills empty spaces with N/A
        self.dataset.drop_duplicates(keep='first', inplace=True)
        self.dataset.fillna('N/A')

    # gets column distribution values
    def col_distribution_values(self, given_column):
        if given_column not in self.dataset.columns:
            return "error"
        return self.dataset[given_column].value_counts()

    # value counter, counts how many values in a given column
    def values_counter(self):
        print("These are the columns available for value counting: \n")
        # for every column in the dataset, prints for user and asks for value count, then prints value count
        for col in self.dataset.columns:
            print(col)
        column=input("Enter the name of a column to count its unique values: \n")
        if column in self.dataset.columns:
            print(f"These are the value counts for {column}: \n{self.dataset[column].value_counts}")

    # calculates the maximum and minimum of a given column
    def min_max_calculater(self):
        # storing all numeric columns
        numeric_columns = self.dataset.select_dtypes(include=['number']).columns
        # printing as option for user
        print("These are the numeric columns in the dataset you can calculate min/maxes for:\n")
        for col in numeric_columns:
            print(col)
        #getting input, and printing min and max
        column = input("Enter the name of the numeric column to calculate the minimum and maximum:\n")
        if column in numeric_columns:
            min_value = self.dataset[column].min()
            max_value = self.dataset[column].max()
            print(f"Minimum of '{column}': {min_value}\nMaximum of '{column}': {max_value}\n")
        else:
            print(f"Column '{column}' is not a numeric column or not found in the dataset.\n")

    # plots a box plot using seaborn and matplotlib
    def box_plotter(self, x_column, y_column, box_title, x_label="", y_label="", figure_size=(10, 6)):
        plt.figure(figsize=figure_size)
        sns.boxplot(x=x_column, y=y_column, data=self.dataset)
        plt.title(box_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    # makes a scatterplot using seaborn and matplotlib
    def scatter_plotter(self, x_column, y_column, scatter_title, x_label="", y_label="", figure_size=(10, 6)):
        plt.figure(figsize=figure_size)
        sns.scatterplot(x=x_column, y=y_column, data=self.dataset)
        plt.title(scatter_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    # makes a violin plot using seaborn and matplotlib
    def violin_plotter(self, x_column, y_column, violin_title, x_label, y_label, figure_size=(10, 6)):
        sns.set_style("whitegrid")
        plt.figure(figsize=figure_size)
        sns.violinplot(x=x_column, y=y_column, data=self.dataset, inner="quartile")
        plt.title(violin_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    # uses all plots for the "showcase" option in analytics
    def graph_showcaser(self):
        print("These are all the types of graphs this program is capable of making with this dataset.\n")
        # separates categorical and numeric columns
        numeric_columns = self.dataset.select_dtypes(include=['number']).columns
        categorical_columns = self.dataset.select_dtypes(include=['object', 'category']).columns
        # if the columns are not empty, it makes the necessary graphs for categorical and numerical data
        if not numeric_columns.empty and not categorical_columns.empty:
            # box plot
            self.box_plotter(categorical_columns[0], numeric_columns[0], f"A Box Plot of {categorical_columns[0]} vs {numeric_columns[0]}")
            # scatter plot
            if len(numeric_columns) > 1:
                self.scatter_plotter(numeric_columns[0], numeric_columns[1], f"A Scatter Plot of {numeric_columns[0]} vs {numeric_columns[1]}")
            # violin plot
            self.violin_plotter(categorical_columns[0], numeric_columns[0], f"A Violin Plot: {categorical_columns[0]} vs {numeric_columns[0]}", categorical_columns[0], numeric_columns[0])
        else:
            print("Sorry, we don't have enough data within this particular dataset to showcase our graph options.\n")

    # gets a random sample of 10 from the dataset
    def sample_caller(self):
        random_sample = []
        while len(random_sample) < 10:
            random_value = r.randrange(0, 365)
            if random_value not in random_sample:
                random_sample.append(random_value)
        data_sample = self.dataset.iloc[random_sample, :]
        print(data_sample)

    # gets a description of columns
    def description_caller(self):
        print(self.data_describer())
        description_col_request = "If you'd like to see the distribution of values for any column, write the name of the column.\nType anything other than a column name or exit to go back to the main menu.\nType 'exit' to exit the application.\n"
        col_request = input(description_col_request)
        if col_request in self.dataset.columns:
            col_request_answer = DataAnalyzer.col_distribution_values(self.dataset, col_request)
            print(col_request_answer)
        elif col_request == 'exit':
            exit()
        else:
            print("That was not a valid column name or the word 'exit'.\nTaking you back to the main menu.")
            pass

    # the tour option
    def tour_caller(self):
        print("Welcome to the data tour! Happy seeing you here, nerds.")
        term = input("Obviously, there's a lot of factors we can consider when looking at our dataset.\nFor this "
                     "program, and this tour, we mainly focus on the affect of different factors on grades in "
                     "each term.\nPlease choose which term you want to focus on for this tour, '1', '2', or '3'.\n")
        while term not in ['1', '2', '3']:
            print("There are only 3 terms.\nPlease try choosing again.\n")
            term = input("Please choose which term you want to focus on for this tour, '1', '2', or '3'.")
        term_name = "G" + term
        # what's the affect of parental education on final grades
        self.box_plotter('Medu', term_name, "EFFECT OF MOTHER'S EDUCATION ON " + term_name,
                                 "Mother's Educational Level", term_name)
        self.box_plotter( 'Fedu', term_name, "EFFECT OF FATHER'S EDUCATION ON " + term_name,
                                 "Father's Educational Level", term_name)
        # what's the relationship between study time and final grades?
        self.box_plotter( 'studytime', term_name,
                                 "RELATIONSHIP BETWEEN STUDY TIME AND " + term_name, 'Study Time',
                                 term_name)
        # what if we compare the final grades by gender?
        self.box_plotter('sex', term_name, "COMPARISON OF " + term_name + " BY GENDER", 'Gender',
                                 term_name)
        # what is the impact of school on student performance?
        self.box_plotter('school', term_name, "IMPACT OF SCHOOL ON STUDENT PERFORMANCE", 'School',
                                 term_name)
        # text conclusion
        print("And that's concludes this little tour! \nHappy exploring!\n\n")
        print("You may now proceed to analyze more, or you can leave:\n")

    # used to go back to main menu, all main menu actions are here
    def interactive(self):
        # the main request prompt
        request_prompt = ("If you'd like a sample of the dataset, type 'sample'.\nIf you'd like a brief description, "
                          "type 'description'.\nIf you'd like to see some data analysis, type 'analytics'.\nIf you'd "
                          "just like an overview of some interesting stuff we've discovered by analyzing our dataset, "
                          "type 'tour'.\nIf you'd like to exit the application, type 'exit'.\n")
        # while the user doesn't exit, this should keep running
        while True:
            # get user input from analysis options
            users_choice = input(request_prompt)
            # based off of the users input, perform various tasks
            match users_choice:
                case 'sample':
                    self.sample_caller()
                case 'description':
                    self.description_caller()
                case 'tour':
                    self.tour_caller()
                    tour_input = input("Type anything to go back to the main menu.\nType 'exit' to leave the "
                                       "application.\n")
                    if tour_input == 'exit':
                        break
                    else:
                        pass
                # most data analysis is within analytics
                case 'analytics':
                    analytics_prompt = ("If you would like to see general descriptive statistics, write "
                                        "'descriptive'.\nIf you'd like to count the number of values in a certain "
                                        "column, type 'count'.\nIf you'd like to calculate the min and max of a "
                                        "column, type 'min n max'.\nIf you'd like to see the types of graphs we can "
                                        "make with this data, type 'showcase'.\nIf you'd like to calculate the "
                                        "average of some column, type 'average'.\nType 'exit' to exit the "
                                        "application.\n")
                    analytics_request = input(analytics_prompt)
                    match analytics_request:
                        case 'descriptive':
                            described_data = DataAnalyzer.data_describer(self)
                            print(described_data)
                            print(self.data_describer())
                            post_descriptive = input("There you have the general descriptive statistics.\nTo go back "
                                                     "to the main menu, type anything.\nTo exit the application type "
                                                     "'exit'.\n")
                            if post_descriptive == 'exit':
                                break
                            else:
                                pass
                        case 'count':
                            self.values_counter()
                        case 'min n max':
                            self.min_max_calculater()
                        case 'showcase':
                            self.graph_showcaser()
                        case 'average':
                            average_calc_df = self.dataset.select_dtypes(include=['int64', 'float64'])
                            numeric_columns = self.dataset.select_dtypes(include=['int64', 'float64']).columns
                            for col in numeric_columns:
                                print(col)
                            column_name = input("Enter the name of the column you want to calculate the average for.\n")
                            if column_name in average_calc_df:
                                average_value = average_calc_df[column_name].mean()
                                print(f"The average for {column_name} is: {average_value}.")
                                print("Taking you back to the main menu now.\n")
                                pass
                            else:
                                print(f"The column {column_name} is not a column, or it is not a numeric column.\nTaking you back to the main menu now.")
                                pass
                        case 'top':
                            top_column_head = self.dataset.select_dtypes(include=['object']).columns
                            for col in top_column_head:
                                print(col)
                            chosen_top_col = input("Please choose one of the binary value storing columns.\n")
                            if chosen_top_col in top_column_head:
                                top_score_min = self.dataset['Numeric Column'].quantile(0.75)
                                top_students = self.dataset[self.dataset['Numeric Column'] >= top_score_min]
                                if chosen_top_col in top_students.columns:
                                    counts = top_students[chosen_top_col].value_counts()
                                    plt.figure(figsize=(8, 8))
                                    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
                                    plt.title(f"Top Students Distribution in {chosen_top_col}")
                                    plt.show()
                                else:
                                    print(f"The column {chosen_top_col} isn't in the top students columns.\n")
                            else:
                                print(f"The column {chosen_top_col} isn't a column.\nOr it's not a binary column.\nTaking you back to the main menu.\n")
                        case 'exit':
                            print("You are leaving this application.\n")
                            break
                        case _:
                            print("That is not a valid request.\nTry again.\n")
                            pass
                case 'exit':
                    print("You are leaving this application.\n")
                    break
                case _:
                    print("That is not a analytics request.\nTaking you back to main menu.\n")
                    pass

                # data cleaning

    # self explanatory, should the user continue or exit the program
    def continue_or_exit(self):
        next_step = input(
            "You may now proceed to analyze more, or you can leave.\nType anything to continue with analysis.\nType 'exit' to leave the application.\n")
        if next_step == 'exit':
            exit()
        else:
            self.interactive()


# run main function
if __name__ == "__main__":
    # for the argsparse
    parser = argparse.ArgumentParser(description="A Tool For Analyzing Student Data From File")
    parser.add_argument('choice', choices=['sample', 'description', 'analytics', 'tour', 'exit'])
    args_choice = parser.parse_args().choice
    # reading the dataset
    data = pd.read_csv("student_data.csv")
    df = pd.DataFrame(data)
    analysis = DataAnalyzer(data)
    # data cleaning
    analysis.data_cleaner()
    # looking through the user input and reacting accordingly
    match args_choice:
        case 'sample':
            analysis.sample_caller()
            analysis.continue_or_exit()
        case 'description':
            print(analysis.data_describer())
            analysis.continue_or_exit()
        case 'analytics':
            analysis.interactive()
        case 'tour':
            analysis.tour_caller()
            analysis.continue_or_exit()
        case _:
            print("That was not a valid input.\nPlease try again.\n")
            analysis.interactive()
# end of code