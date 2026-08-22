from abc import ABC, abstractmethod


class DataLoader(ABC):

    @abstractmethod
    def load(self, cleaned_df,output_file):
        pass