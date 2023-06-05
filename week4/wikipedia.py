import sys
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        self.keys = []

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
                self.keys.append(id)
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def get_keys_from_value(d, val):
        return [k for k, v in d.items() if v == val]

    def get_key_from_value(d, val):
        keys = [k for k, v in d.items() if v == val]
        if keys:
            return keys[0]
        return None

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        queue = deque()
        queue.append(start)

        # Keep track of which nodes have been visited
        visited = {}
        visited[start] = True

        # Keep track of how many steps have been taken to reach the node
        before = {}
        before[start] = None

        while not len(queue) == 0:
            node = queue.popleft()

            for child_index in self.links[Wikipedia.get_key_from_value(self.titles, node)]:
                child = self.titles[child_index]
                if child  == goal:
                    visit_order = []
                    visit_order.append(node)
                    visit_order.append(goal)

                    tmp = node
                    while tmp != start:
                        visit_order.insert(0, before[tmp])
                        tmp = before[tmp]

                    print("The shortest path from ", start , "to " , goal,"is:")
                    for i in range(len(visit_order)):
                        print(visit_order[i])
                    print()
                    return

                if not child in visited:
                    visited[child] = True
                    before[child] = node
                    queue.append(child)

        print("Not Found")
        print()
        return


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        pagerank = dict(zip(self.keys, len(self.titles) * [1.0]))

        for i in range(10000):
            next_pagerank = dict(zip(self.keys, len(self.titles) * [0.0]))
            for i in range(len(self.titles)):
                if not self.keys[i] in self.links:
                    next_pagerank = dict(zip(self.keys, len(self.titles) * [pagerank[self.keys[i]] / len(self.titles)]))
                else:
                    for j in range(len(self.links[self.keys[i]])):
                        next_pagerank[self.links[self.keys[i]][j]] += 0.85 * pagerank[self.keys[i]] / len(self.links[self.keys[i]])
            for i in range(len(self.titles)):
                next_pagerank[self.keys[i]] += 0.15

            # If the norm of the difference of pagerank and next_pagerank is less than 0.1, break the manipulation
            norm = 0
            pagerank_values = list(pagerank.values())
            next_page_rank_values = list(next_pagerank.values())
            for i in range(len(pagerank_values)):
                norm += (pagerank_values[i] - next_page_rank_values[i])**2

            if norm < 0.001:
                break
            else:
                pagerank = next_pagerank

        max_index = 0
        for i in range(1, len(pagerank)):
            if pagerank[self.keys[max_index]] < pagerank[self.keys[i]]:
                max_index = i

        print("The most important page is:")
        print(self.titles[self.keys[max_index]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()