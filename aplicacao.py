from cassandra.cluster import Cluster

class CassandraClient:
    def __init__(self, contact_points, keyspace):
        self.cluster = Cluster(contact_points=contact_points)
        self.session = self.cluster.connect(keyspace)

    def insert_book(self, id, title, author, year):
        query = "INSERT INTO livros (id, titulo, autor, ano_publicacao) VALUES (%s, %s, %s, %s)"
        self.session.execute(query, (id, title, author, year))
        print("Livro inserido com sucesso!")

    def get_all_books(self):
        query = "SELECT * FROM livros"
        result = self.session.execute(query)
        for row in result:
            print(row)

    def search_books_by_author(self, author):
        query = "SELECT * FROM livros WHERE autor = %s"
        result = self.session.execute(query, (author,))
        for row in result:
            print(row)

    def search_books_by_title(self, title):
        query = "SELECT * FROM livros WHERE titulo = %s"
        result = self.session.execute(query, (title,))
        for row in result:
            print(row)

    def close(self):
        self.cluster.shutdown()

def main():
    contact_points = ['localhost']  # Use o IP do seu container Cassandra
    keyspace = "biblioteca"

    client = CassandraClient(contact_points, keyspace)

    while True:
        print("\nEscolha uma opção:")
        print("1. Inserir um novo livro")
        print("2. Listar todos os livros")
        print("3. Pesquisar livros por autor")
        print("4. Pesquisar livros por título")
        print("5. Sair")

        choice = input("Digite o número da opção desejada: ")

        if choice == '1':
            id = input("Digite o ID do livro: ")
            title = input("Digite o título do livro: ")
            author = input("Digite o autor do livro: ")
            year = input("Digite o ano de publicação do livro: ")
            client.insert_book(id, title, author, year)

        elif choice == '2':
            print("\nTodos os livros:")
            client.get_all_books()

        elif choice == '3':
            author = input("Digite o nome do autor: ")
            print("\nLivros por autor:")
            client.search_books_by_author(author)

        elif choice == '4':
            title = input("Digite o título do livro: ")
            print("\nLivros por título:")
            client.search_books_by_title(title)

        elif choice == '5':
            break

        else:
            print("Opção inválida. Digite um número de 1 a 5.")

    client.close()

if __name__ == "__main__":
    main()