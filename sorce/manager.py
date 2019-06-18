#coding:utf-8

from abc import ABCMeta, abstractmethod
import json
import csv


class Manager(metaclass=ABCMeta):
    @abstractmethod
    def make_file(self, data, filename):
        pass

    @abstractmethod
    def load_file(self, filename):
        pass


class TxtManager(Manager):
    def make_file(self, data, filename):
        with open(filename, 'w') as txtfile:
            if type(data) is list:
                txtfile.writelines(data)
            elif type(data) is str:
                txtfile.write(data)
    
    def load_file(self, filename):
        with open(filename, 'r') as txtfile:
            text = txtfile.readlines()
        
        return text

class JsonManager(Manager):
    def make_file(self, data, filename):
        if type(data) is not dict:
            print("type error")
            exit

        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile)

    def load_file(self, filename):
        with open(filename, 'r') as jsonfile:
            json_dict = json.load(jsonfile)

        return json_dict


class CsvManager(Manager):
    def make_file(self, data, filename):
        if type(data) is not list:
            print("type error")
            exit

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def load_file(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            csv_list = [row for row in reader]

        return csv_list
