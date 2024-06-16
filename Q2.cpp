#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <sstream>

using namespace std;

// Function to read a dataset from a text file
vector<int> read_dataset(const string& filename) {
    vector<int> data;
    ifstream file(filename);
    if (!file) {
        cerr << "Could not open the file " << filename << endl;
        return data;
    }
    int number;
    while (file >> number) {
        data.push_back(number);
    }
    return data;
}

// Function to write a list of numbers to a text file
void write_to_file(const string& filename, const vector<int>& data) {
    ofstream file(filename);
    if (!file) {
        cerr << "Could not open the file " << filename << endl;
        return;
    }
    for (const int& number : data) {
        file << number << "\n";
    }
}

// Heapify function to maintain heap property (in-place modification)
void heapify(vector<int>& arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }

    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

// Heap sort function
void heap_sort(vector<int>& arr) {
    int n = arr.size();

    // Build a maxheap from the input array (in-place)
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }

    // One by one extract an element from heap (in-place)
    for (int i = n - 1; i > 0; i--) {
        swap(arr[i], arr[0]);
        heapify(arr, i, 0);
    }
}

// Selection sort function
void selection_sort(vector<int>& arr) {
    int n = arr.size();
    for (int i = n - 1; i > 0; i--) { 
        int max_index = i;
        for (int j = 0; j < i; j++) {
            if (arr[j] > arr[max_index]) {
                max_index = j;
            }
        }
        if (max_index != i) {
            swap(arr[i], arr[max_index]);
        }
    }
}

int main() {
    vector<int> dataset_sizes = {100, 1000, 10000, 100000, 500000, 1000000};
    vector<string> dataset_filenames;

    for (int size : dataset_sizes) {
        dataset_filenames.push_back("dataset_" + to_string(size) + ".txt");
    }

    // Process heap sort for all datasets first
    for (const string& dataset_filename : dataset_filenames) {
        vector<int> dataset = read_dataset(dataset_filename);
        if (dataset.empty()) {
            cout << "Skipping dataset: " << dataset_filename << endl;
            continue;
        }

        auto start_enqueue = chrono::high_resolution_clock::now();
        // Build max heap
        for (int i = dataset.size() / 2 - 1; i >= 0; i--) {
            heapify(dataset, dataset.size(), i);
        }
        auto end_enqueue = chrono::high_resolution_clock::now();
        chrono::duration<double> enqueue_time = end_enqueue - start_enqueue;

        auto start_dequeue = chrono::high_resolution_clock::now();
        // Sort the heap
        for (int i = dataset.size() - 1; i > 0; i--) {
            swap(dataset[0], dataset[i]);
            heapify(dataset, i, 0);
        }
        auto end_dequeue = chrono::high_resolution_clock::now();
        chrono::duration<double> dequeue_time = end_dequeue - start_dequeue;

        string heap_sorted_filename = "heap_sorted_" + dataset_filename;
        write_to_file(heap_sorted_filename, dataset);

        cout << "Heap Sort : " << dataset_filename << endl;
        cout << "Heap Sort Enqueue Time: " << enqueue_time.count() << " seconds" << endl;
        cout << "Heap Sort Dequeue Time: " << dequeue_time.count() << " seconds" << endl;
        cout << "--------------------------------------------------" << endl;
    }

    // Now process selection sort for all datasets
    for (const string& dataset_filename : dataset_filenames) {
        vector<int> dataset = read_dataset(dataset_filename);
        if (dataset.empty()) {
            cout << "Skipping dataset: " << dataset_filename << endl;
            continue;
        }

        auto start = chrono::high_resolution_clock::now();
        selection_sort(dataset);
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> selection_sort_time = end - start;

        string selection_sorted_filename = "selection_sorted_" + dataset_filename;
        write_to_file(selection_sorted_filename, dataset);

        cout << "Selection Sort Dataset: " << dataset_filename << endl;
        cout << "Selection Sort Time: " << selection_sort_time.count() << " seconds" << endl;
        cout << "--------------------------------------------------" << endl;
    }

    return 0;
}