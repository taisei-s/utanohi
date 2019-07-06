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
        if type(data) is list:
            with open(filename, 'w') as txtfile:
                txtfile.writelines(data)
        elif type(data) is str:
            with open(filename, 'w') as txtfile:
                txtfile.write(data)
        else:
            raise AttributeError("data type '{}' can't write file in this method. please use data type str or list".format(type(data)))

    def load_file(self, filename):
        with open(filename, 'r') as txtfile:
            text = txtfile.readlines()
        return text

    def add_file(self, data, filename):
        if type(data) is list:
            with open(filename, 'a') as txtfile:
                txtfile.writelines(data)
        elif type(data) is str:
            with open(filename, 'a') as txtfile:
                txtfile.write(data)
        else:
            raise AttributeError("data type '{}' can't write file in this method. please use data type str or list".format(type(data)))

class JsonManager(Manager):
    def make_file(self, data, filename):
        if type(data) is not dict:
            raise AttributeError("data type '{}' can't write file in this method. please use data type dict".format(type(data)))

        text = json.dumps(data, sort_keys=False, ensure_ascii=False, indent=2)
        with open(filename, 'w') as jsonfile:
            jsonfile.write(text)

    def load_file(self, filename):
        with open(filename, 'r') as jsonfile:
            json_dict = json.load(jsonfile)
        return json_dict


class CsvManager(Manager):
    def make_file(self, data, filename):
        if type(data) is not list:
            raise AttributeError("data type '{}' can't write file in this method. please use data type list".format(type(data)))

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if isinstance(data[0], list) is False:
                writer.writerow(data)
            else:
                writer.writerows(data)

    def load_file(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            csv_list = [row for row in reader]
        return csv_list

    def add_file(self, data, filename):
        if type(data) is not list:
            raise AttributeError("data type '{}' can't write file in this method. please use data type list".format(type(data)))

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if isinstance(data[0], list) is False:
                writer.writerow(data)
            else:
                writer.writerows(data)


if __name__ == "__main__":
    test = [[1, 2, 3, 4], [1, 2, 3, 4]]
    csvtest = CsvManager()
    csvtest.add_file(test, 'test.csv')