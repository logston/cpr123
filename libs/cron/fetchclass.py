from libs.fetch.fetchclass import FetchClass

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        class_id = sys.argv[1]
    else:
        class_id = '198654'

results = FetchClass().fetch_class(class_id)
print('Results for class id ', class_id)
print(results)
