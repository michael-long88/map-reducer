from map_reducer import MapReducer, Reducer, Mapper
import time

if __name__ == '__main__':
    word_file = r"dickinson.txt"
    start_time = time.time()
    text_reader = Mapper(word_file)
    text_reader.read_text()
    reducer = Reducer(text_reader.hash_maps)
    reducer.reduce()
    end_time = time.time()
    hash_map_total_time = end_time - start_time
    print(reducer.get_top_ten_words())
    print(f"Took {hash_map_total_time} seconds")

    start_time = time.time()
    map_reducer = MapReducer(word_file)
    map_reducer.read_text()
    map_reducer.reduce()
    end_time = time.time()
    dictionary_total_time = end_time - start_time
    print(map_reducer.get_top_ten_words())
    print(f"Took {dictionary_total_time} seconds")

    if dictionary_total_time < hash_map_total_time:
        print(f"Dictionary processing was faster by {hash_map_total_time - dictionary_total_time} seconds")
    else:
        print(f"Hash map processing was faster by {dictionary_total_time - hash_map_total_time} seconds")