import pandas as pd

class classname():
    @staticmethod
    def univariate(dataset):
        Qual = []
        Quan = []
        for columnName in dataset:
            if dataset[columnName].dtypes == 'O':
                Qual.append(columnName)
            else:
                Quan.append(columnName)
        return Qual, Quan

    @staticmethod
    def central_tendency_IQR(dataset, Quan):
        descriptive = pd.DataFrame(index=['Mean', 'Median', 'Mode', 'Q1:25%', 'Q2:50%', 'Q3:75%', 'Q4:100%', 'IQR', 'Lesser IQR', 'Greater IQR', 'min', 'max', 'kurtosis', 'skew','var','std'], columns=Quan)
    
        for columnName in Quan:
            descriptive.loc["Mean", columnName] = dataset[columnName].mean()
            descriptive.loc["Median", columnName] = dataset[columnName].median()
            descriptive.loc["Mode", columnName] = dataset[columnName].mode()[0]
            descriptive.loc["Q1:25%", columnName] = dataset[columnName].quantile(0.25)
            descriptive.loc["Q2:50%", columnName] = dataset[columnName].quantile(0.50)
            descriptive.loc["Q3:75%", columnName] = dataset[columnName].quantile(0.75)
            descriptive.loc["Q4:100%", columnName] = dataset[columnName].max()
            descriptive.loc["IQR", columnName] = dataset[columnName].quantile(0.75) - dataset[columnName].quantile(0.25)
            descriptive.loc["Lesser IQR", columnName] = dataset[columnName].quantile(0.25) - 1.5 * (dataset[columnName].quantile(0.75) - dataset[columnName].quantile(0.25))
            descriptive.loc["Greater IQR", columnName] = dataset[columnName].quantile(0.75) + 1.5 * (dataset[columnName].quantile(0.75) - dataset[columnName].quantile(0.25))
            descriptive.loc["min", columnName] = dataset[columnName].min()
            descriptive.loc["max", columnName] = dataset[columnName].max()
            descriptive.loc["kurtosis", columnName] = dataset[columnName].kurtosis()
            descriptive.loc["skew", columnName] = dataset[columnName].skew()
            descriptive.loc["var", columnName] = dataset[columnName].var()
            descriptive.loc["std", columnName] = dataset[columnName].std()
        return descriptive

    @staticmethod
    def check_outliers(dataset, descriptive, Quan):  # Add dataset parameter
        lesser = []
        greater = []

        # Check for outliers
        for columnName in Quan:
            if descriptive.loc['Lesser IQR', columnName] > descriptive.loc['min', columnName]:
                lesser.append(columnName)

            if descriptive.loc['Greater IQR', columnName] < descriptive.loc['max', columnName]:
                greater.append(columnName)

        return lesser, greater

    @staticmethod
    def replace_outliers(dataset, descriptive, lesser, greater):
        for columnName in lesser:
            dataset.loc[dataset[columnName] < descriptive.loc['Lesser IQR', columnName], columnName] = descriptive.loc['Lesser IQR', columnName]

        for columnName in greater:
            dataset.loc[dataset[columnName] > descriptive.loc['Greater IQR', columnName], columnName] = descriptive.loc['Greater IQR', columnName]

        return dataset

    @staticmethod
    def recheck_outliers_after_replace(dataset, descriptive, Quan):
        recheck_lesser = []
        recheck_greater = []

        # Check for outliers after replacement
        for columnName in Quan:
            if descriptive.loc['Lesser IQR', columnName] > descriptive.loc['min', columnName]:
                recheck_lesser.append(columnName)

            if descriptive.loc['Greater IQR', columnName] < descriptive.loc['max', columnName]:
                recheck_greater.append(columnName)

        return recheck_lesser, recheck_greater

    # Freq, Relative Freq, Cumulative Freq
    def freqTable(dataset, columnName):
        freqTable = pd.DataFrame(columns=["Unique_values","Freq","Relative_freq","Cumulative_freq"])
        # Calculate frequencies of values in the 'ssc_p' column
        freqTable["Unique_values"] = dataset[columnName].value_counts().index
        freqTable["Freq"] = dataset[columnName].value_counts().values
        
        # Calculate total count
        total_count = freqTable['Freq'].sum()
        
        # Calculate relative frequency and add to freqTable
        freqTable["Relative_freq"] = (freqTable["Freq"] / total_count) * 100
        
        # Calculate cumulative frequency
        freqTable["Cumulative_freq"] = freqTable["Relative_freq"].cumsum()
    
        return freqTable
