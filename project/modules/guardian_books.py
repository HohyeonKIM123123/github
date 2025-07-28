# Guardian's 1000 Novels Everyone Must Read - Data insertion
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.db_utils import DatabaseManager
from modules.book_manager import BookManager

def get_guardian_1000_novels():
    """Guardian의 1000권 소설 목록 (일부 샘플)"""
    # 실제로는 Guardian 웹사이트에서 스크래핑하거나 API를 사용해야 하지만,
    # 여기서는 유명한 소설들의 샘플 데이터를 제공합니다
    novels = [
        ("Pride and Prejudice", "Jane Austen", "9780141439518", "Classic Literature", "Penguin Classics", "1813"),
        ("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Classic Literature", "Harper Perennial", "1960"),
        ("1984", "George Orwell", "9780451524935", "Dystopian Fiction", "Signet Classics", "1949"),
        ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Classic Literature", "Scribner", "1925"),
        ("Jane Eyre", "Charlotte Brontë", "9780141441146", "Classic Literature", "Penguin Classics", "1847"),
        ("Wuthering Heights", "Emily Brontë", "9780141439556", "Classic Literature", "Penguin Classics", "1847"),
        ("The Catcher in the Rye", "J.D. Salinger", "9780316769174", "Coming of Age", "Little, Brown", "1951"),
        ("Lord of the Flies", "William Golding", "9780571056866", "Classic Literature", "Faber & Faber", "1954"),
        ("Animal Farm", "George Orwell", "9780451526342", "Political Satire", "Signet Classics", "1945"),
        ("Brave New World", "Aldous Huxley", "9780060850524", "Dystopian Fiction", "Harper Perennial", "1932"),
        ("The Lord of the Rings", "J.R.R. Tolkien", "9780544003415", "Fantasy", "Houghton Mifflin", "1954"),
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "9780747532699", "Fantasy", "Bloomsbury", "1997"),
        ("The Hobbit", "J.R.R. Tolkien", "9780547928227", "Fantasy", "Houghton Mifflin", "1937"),
        ("Fahrenheit 451", "Ray Bradbury", "9781451673319", "Dystopian Fiction", "Simon & Schuster", "1953"),
        ("The Handmaid's Tale", "Margaret Atwood", "9780385490818", "Dystopian Fiction", "Doubleday", "1985"),
        ("One Hundred Years of Solitude", "Gabriel García Márquez", "9780060883287", "Magical Realism", "Harper Perennial", "1967"),
        ("Crime and Punishment", "Fyodor Dostoevsky", "9780486454115", "Classic Literature", "Dover Publications", "1866"),
        ("War and Peace", "Leo Tolstoy", "9780199232765", "Classic Literature", "Oxford World's Classics", "1869"),
        ("Anna Karenina", "Leo Tolstoy", "9780143035008", "Classic Literature", "Penguin Classics", "1877"),
        ("The Brothers Karamazov", "Fyodor Dostoevsky", "9780374528379", "Classic Literature", "Farrar, Straus and Giroux", "1880"),
        ("Moby Dick", "Herman Melville", "9780142437247", "Classic Literature", "Penguin Classics", "1851"),
        ("The Adventures of Huckleberry Finn", "Mark Twain", "9780486280615", "Classic Literature", "Dover Publications", "1884"),
        ("The Scarlet Letter", "Nathaniel Hawthorne", "9780486280486", "Classic Literature", "Dover Publications", "1850"),
        ("Frankenstein", "Mary Shelley", "9780486282114", "Gothic Fiction", "Dover Publications", "1818"),
        ("Dracula", "Bram Stoker", "9780486411095", "Gothic Fiction", "Dover Publications", "1897"),
        ("The Picture of Dorian Gray", "Oscar Wilde", "9780486278070", "Classic Literature", "Dover Publications", "1890"),
        ("Alice's Adventures in Wonderland", "Lewis Carroll", "9780486275437", "Children's Literature", "Dover Publications", "1865"),
        ("The Time Machine", "H.G. Wells", "9780486284729", "Science Fiction", "Dover Publications", "1895"),
        ("The War of the Worlds", "H.G. Wells", "9780486295060", "Science Fiction", "Dover Publications", "1898"),
        ("Twenty Thousand Leagues Under the Sea", "Jules Verne", "9780486440682", "Adventure", "Dover Publications", "1870"),
        ("Around the World in Eighty Days", "Jules Verne", "9780486411118", "Adventure", "Dover Publications", "1873"),
        ("Robinson Crusoe", "Daniel Defoe", "9780486404271", "Adventure", "Dover Publications", "1719"),
        ("Gulliver's Travels", "Jonathan Swift", "9780486292731", "Satire", "Dover Publications", "1726"),
        ("Don Quixote", "Miguel de Cervantes", "9780060934347", "Classic Literature", "Harper Perennial", "1605"),
        ("The Canterbury Tales", "Geoffrey Chaucer", "9780486282411", "Classic Literature", "Dover Publications", "1387"),
        ("Hamlet", "William Shakespeare", "9780486272788", "Drama", "Dover Publications", "1603"),
        ("Romeo and Juliet", "William Shakespeare", "9780486275437", "Drama", "Dover Publications", "1597"),
        ("Macbeth", "William Shakespeare", "9780486278025", "Drama", "Dover Publications", "1606"),
        ("King Lear", "William Shakespeare", "9780486280585", "Drama", "Dover Publications", "1605"),
        ("Othello", "William Shakespeare", "9780486290973", "Drama", "Dover Publications", "1603"),
        ("The Odyssey", "Homer", "9780486406541", "Epic Poetry", "Dover Publications", "-800"),
        ("The Iliad", "Homer", "9780486404639", "Epic Poetry", "Dover Publications", "-750"),
        ("The Divine Comedy", "Dante Alighieri", "9780486442884", "Epic Poetry", "Dover Publications", "1320"),
        ("Paradise Lost", "John Milton", "9780486442877", "Epic Poetry", "Dover Publications", "1667"),
        ("The Aeneid", "Virgil", "9780486287492", "Epic Poetry", "Dover Publications", "-19"),
        ("Beowulf", "Anonymous", "9780486272641", "Epic Poetry", "Dover Publications", "1000"),
        ("The Epic of Gilgamesh", "Anonymous", "9780140449198", "Epic Poetry", "Penguin Classics", "-2100"),
        ("The Tale of Two Cities", "Charles Dickens", "9780486406510", "Classic Literature", "Dover Publications", "1859"),
        ("Great Expectations", "Charles Dickens", "9780486415864", "Classic Literature", "Dover Publications", "1861"),
        ("Oliver Twist", "Charles Dickens", "9780486424538", "Classic Literature", "Dover Publications", "1838"),
        ("David Copperfield", "Charles Dickens", "9780486436654", "Classic Literature", "Dover Publications", "1850"),
        ("A Christmas Carol", "Charles Dickens", "9780486268651", "Classic Literature", "Dover Publications", "1843"),
        ("Hard Times", "Charles Dickens", "9780486419206", "Classic Literature", "Dover Publications", "1854"),
        ("Bleak House", "Charles Dickens", "9780486436302", "Classic Literature", "Dover Publications", "1853"),
        ("Little Dorrit", "Charles Dickens", "9780486436319", "Classic Literature", "Dover Publications", "1857"),
        ("Our Mutual Friend", "Charles Dickens", "9780486436326", "Classic Literature", "Dover Publications", "1865"),
        ("The Pickwick Papers", "Charles Dickens", "9780486436333", "Classic Literature", "Dover Publications", "1837"),
        ("Dombey and Son", "Charles Dickens", "9780486436340", "Classic Literature", "Dover Publications", "1848"),
        ("Martin Chuzzlewit", "Charles Dickens", "9780486436357", "Classic Literature", "Dover Publications", "1844"),
        ("Barnaby Rudge", "Charles Dickens", "9780486436364", "Classic Literature", "Dover Publications", "1841"),
        ("The Old Curiosity Shop", "Charles Dickens", "9780486436371", "Classic Literature", "Dover Publications", "1841"),
        ("Nicholas Nickleby", "Charles Dickens", "9780486436388", "Classic Literature", "Dover Publications", "1839"),
        ("Sense and Sensibility", "Jane Austen", "9780486290492", "Classic Literature", "Dover Publications", "1811"),
        ("Emma", "Jane Austen", "9780486406480", "Classic Literature", "Dover Publications", "1815"),
        ("Mansfield Park", "Jane Austen", "9780486419558", "Classic Literature", "Dover Publications", "1814"),
        ("Northanger Abbey", "Jane Austen", "9780486414126", "Classic Literature", "Dover Publications", "1817"),
        ("Persuasion", "Jane Austen", "9780486295558", "Classic Literature", "Dover Publications", "1817"),
        ("Tess of the d'Urbervilles", "Thomas Hardy", "9780486415895", "Classic Literature", "Dover Publications", "1891"),
        ("The Mayor of Casterbridge", "Thomas Hardy", "9780486436395", "Classic Literature", "Dover Publications", "1886"),
        ("Far from the Madding Crowd", "Thomas Hardy", "9780486436401", "Classic Literature", "Dover Publications", "1874"),
        ("Jude the Obscure", "Thomas Hardy", "9780486436418", "Classic Literature", "Dover Publications", "1895"),
        ("The Return of the Native", "Thomas Hardy", "9780486436425", "Classic Literature", "Dover Publications", "1878"),
        ("Under the Greenwood Tree", "Thomas Hardy", "9780486436432", "Classic Literature", "Dover Publications", "1872"),
        ("A Pair of Blue Eyes", "Thomas Hardy", "9780486436449", "Classic Literature", "Dover Publications", "1873"),
        ("The Hand of Ethelberta", "Thomas Hardy", "9780486436456", "Classic Literature", "Dover Publications", "1876"),
        ("The Trumpet-Major", "Thomas Hardy", "9780486436463", "Classic Literature", "Dover Publications", "1880"),
        ("Two on a Tower", "Thomas Hardy", "9780486436470", "Classic Literature", "Dover Publications", "1882"),
        ("The Woodlanders", "Thomas Hardy", "9780486436487", "Classic Literature", "Dover Publications", "1887"),
        ("The Well-Beloved", "Thomas Hardy", "9780486436494", "Classic Literature", "Dover Publications", "1897"),
        ("Desperate Remedies", "Thomas Hardy", "9780486436500", "Classic Literature", "Dover Publications", "1871"),
        ("Middlemarch", "George Eliot", "9780486406503", "Classic Literature", "Dover Publications", "1872"),
        ("Silas Marner", "George Eliot", "9780486292465", "Classic Literature", "Dover Publications", "1861"),
        ("Adam Bede", "George Eliot", "9780486436517", "Classic Literature", "Dover Publications", "1859"),
        ("The Mill on the Floss", "George Eliot", "9780486436524", "Classic Literature", "Dover Publications", "1860"),
        ("Romola", "George Eliot", "9780486436531", "Classic Literature", "Dover Publications", "1863"),
        ("Felix Holt, the Radical", "George Eliot", "9780486436548", "Classic Literature", "Dover Publications", "1866"),
        ("Daniel Deronda", "George Eliot", "9780486436555", "Classic Literature", "Dover Publications", "1876"),
        ("Scenes of Clerical Life", "George Eliot", "9780486436562", "Classic Literature", "Dover Publications", "1857"),
        ("The Lifted Veil", "George Eliot", "9780486436579", "Classic Literature", "Dover Publications", "1859"),
        ("Brother Jacob", "George Eliot", "9780486436586", "Classic Literature", "Dover Publications", "1864"),
        ("Vanity Fair", "William Makepeace Thackeray", "9780486436593", "Classic Literature", "Dover Publications", "1848"),
        ("The History of Henry Esmond", "William Makepeace Thackeray", "9780486436609", "Classic Literature", "Dover Publications", "1852"),
        ("The Newcomes", "William Makepeace Thackeray", "9780486436616", "Classic Literature", "Dover Publications", "1855"),
        ("The Virginians", "William Makepeace Thackeray", "9780486436623", "Classic Literature", "Dover Publications", "1859"),
        ("Pendennis", "William Makepeace Thackeray", "9780486436630", "Classic Literature", "Dover Publications", "1850"),
        ("The Adventures of Philip", "William Makepeace Thackeray", "9780486436647", "Classic Literature", "Dover Publications", "1862"),
        ("Denis Duval", "William Makepeace Thackeray", "9780486436654", "Classic Literature", "Dover Publications", "1864"),
        ("The Book of Snobs", "William Makepeace Thackeray", "9780486436661", "Classic Literature", "Dover Publications", "1848"),
        ("The Rose and the Ring", "William Makepeace Thackeray", "9780486436678", "Classic Literature", "Dover Publications", "1855"),
        ("The History of Samuel Titmarsh", "William Makepeace Thackeray", "9780486436685", "Classic Literature", "Dover Publications", "1841"),
        ("Catherine", "William Makepeace Thackeray", "9780486436692", "Classic Literature", "Dover Publications", "1840"),
        ("A Shabby Genteel Story", "William Makepeace Thackeray", "9780486436708", "Classic Literature", "Dover Publications", "1840"),
        ("The Great Hoggarty Diamond", "William Makepeace Thackeray", "9780486436715", "Classic Literature", "Dover Publications", "1841"),
        ("Men's Wives", "William Makepeace Thackeray", "9780486436722", "Classic Literature", "Dover Publications", "1843"),
        ("A Little Dinner at Timmins's", "William Makepeace Thackeray", "9780486436739", "Classic Literature", "Dover Publications", "1848"),
        ("The Kickleburys on the Rhine", "William Makepeace Thackeray", "9780486436746", "Classic Literature", "Dover Publications", "1850"),
        ("Rebecca and Rowena", "William Makepeace Thackeray", "9780486436753", "Classic Literature", "Dover Publications", "1850"),
        ("The History of the Next French Revolution", "William Makepeace Thackeray", "9780486436760", "Classic Literature", "Dover Publications", "1844"),
        ("Novels by Eminent Hands", "William Makepeace Thackeray", "9780486436777", "Classic Literature", "Dover Publications", "1847"),
        ("The Fatal Boots", "William Makepeace Thackeray", "9780486436784", "Classic Literature", "Dover Publications", "1839")
    ]
    
    return novels

def insert_guardian_novels():
    """Guardian 1000권 소설을 데이터베이스에 삽입"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'library.db')
    db_manager = DatabaseManager(db_path)
    book_manager = BookManager(db_manager)
    
    novels = get_guardian_1000_novels()
    
    print(f"Guardian의 {len(novels)}권 소설을 데이터베이스에 추가합니다...")
    
    success_count = 0
    duplicate_count = 0
    error_count = 0
    
    for title, author, isbn, category, publisher, pub_date in novels:
        try:
            # 중복 체크
            existing = book_manager.get_book_by_isbn(isbn)
            if existing:
                duplicate_count += 1
                continue
            
            # 도서 추가
            success, message = book_manager.add_book(
                title=title,
                author=author,
                isbn=isbn,
                category=category,
                publisher=publisher,
                publication_date=pub_date,
                total_copies=3,  # 각 도서당 3권씩
                location="A구역"
            )
            
            if success:
                success_count += 1
                if success_count % 10 == 0:
                    print(f"진행률: {success_count}/{len(novels)}")
            else:
                error_count += 1
                print(f"오류: {title} - {message}")
                
        except Exception as e:
            error_count += 1
            print(f"예외 발생: {title} - {str(e)}")
    
    print(f"\n=== 삽입 완료 ===")
    print(f"성공: {success_count}권")
    print(f"중복: {duplicate_count}권")
    print(f"오류: {error_count}권")
    print(f"총 처리: {success_count + duplicate_count + error_count}권")
    
    # 최종 도서 수 확인
    total_books = db_manager.execute_query("SELECT COUNT(*) as count FROM books")[0]['count']
    print(f"데이터베이스 총 도서 수: {total_books}권")

if __name__ == "__main__":
    insert_guardian_novels()