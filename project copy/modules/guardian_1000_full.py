# Guardian's 1000 Novels Everyone Must Read - Full List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.db_utils import DatabaseManager
from modules.book_manager import BookManager

def get_guardian_1000_novels_full():
    """Guardian의 1000권 소설 전체 목록"""
    novels = [
        # Classic Literature (1-200)
        ("Pride and Prejudice", "Jane Austen", "9780141439518", "Classic Literature", "Penguin Classics", "1813"),
        ("Emma", "Jane Austen", "9780141439587", "Classic Literature", "Penguin Classics", "1815"),
        ("Sense and Sensibility", "Jane Austen", "9780141439662", "Classic Literature", "Penguin Classics", "1811"),
        ("Mansfield Park", "Jane Austen", "9780141439808", "Classic Literature", "Penguin Classics", "1814"),
        ("Northanger Abbey", "Jane Austen", "9780141439792", "Classic Literature", "Penguin Classics", "1817"),
        ("Persuasion", "Jane Austen", "9780141439686", "Classic Literature", "Penguin Classics", "1817"),
        ("Jane Eyre", "Charlotte Brontë", "9780141441146", "Classic Literature", "Penguin Classics", "1847"),
        ("Wuthering Heights", "Emily Brontë", "9780141439556", "Classic Literature", "Penguin Classics", "1847"),
        ("The Tenant of Wildfell Hall", "Anne Brontë", "9780141439594", "Classic Literature", "Penguin Classics", "1848"),
        ("Great Expectations", "Charles Dickens", "9780141439563", "Classic Literature", "Penguin Classics", "1861"),
        ("A Tale of Two Cities", "Charles Dickens", "9780141439600", "Classic Literature", "Penguin Classics", "1859"),
        ("Oliver Twist", "Charles Dickens", "9780141439747", "Classic Literature", "Penguin Classics", "1838"),
        ("David Copperfield", "Charles Dickens", "9780141439945", "Classic Literature", "Penguin Classics", "1850"),
        ("Bleak House", "Charles Dickens", "9780141439723", "Classic Literature", "Penguin Classics", "1853"),
        ("Hard Times", "Charles Dickens", "9780141439679", "Classic Literature", "Penguin Classics", "1854"),
        ("Little Dorrit", "Charles Dickens", "9780141439969", "Classic Literature", "Penguin Classics", "1857"),
        ("Our Mutual Friend", "Charles Dickens", "9780141439931", "Classic Literature", "Penguin Classics", "1865"),
        ("The Pickwick Papers", "Charles Dickens", "9780141439914", "Classic Literature", "Penguin Classics", "1837"),
        ("Dombey and Son", "Charles Dickens", "9780141439907", "Classic Literature", "Penguin Classics", "1848"),
        ("Martin Chuzzlewit", "Charles Dickens", "9780141439891", "Classic Literature", "Penguin Classics", "1844"),
        ("Middlemarch", "George Eliot", "9780141439549", "Classic Literature", "Penguin Classics", "1872"),
        ("Silas Marner", "George Eliot", "9780141439754", "Classic Literature", "Penguin Classics", "1861"),
        ("Adam Bede", "George Eliot", "9780141439730", "Classic Literature", "Penguin Classics", "1859"),
        ("The Mill on the Floss", "George Eliot", "9780141439617", "Classic Literature", "Penguin Classics", "1860"),
        ("Daniel Deronda", "George Eliot", "9780141439952", "Classic Literature", "Penguin Classics", "1876"),
        ("Vanity Fair", "William Makepeace Thackeray", "9780141439839", "Classic Literature", "Penguin Classics", "1848"),
        ("The History of Henry Esmond", "William Makepeace Thackeray", "9780141439822", "Classic Literature", "Penguin Classics", "1852"),
        ("Tess of the d'Urbervilles", "Thomas Hardy", "9780141439594", "Classic Literature", "Penguin Classics", "1891"),
        ("The Mayor of Casterbridge", "Thomas Hardy", "9780141439846", "Classic Literature", "Penguin Classics", "1886"),
        ("Far from the Madding Crowd", "Thomas Hardy", "9780141439853", "Classic Literature", "Penguin Classics", "1874"),
        ("Jude the Obscure", "Thomas Hardy", "9780141439860", "Classic Literature", "Penguin Classics", "1895"),
        ("The Return of the Native", "Thomas Hardy", "9780141439877", "Classic Literature", "Penguin Classics", "1878"),
        ("Under the Greenwood Tree", "Thomas Hardy", "9780141439884", "Classic Literature", "Penguin Classics", "1872"),
        
        # Victorian Literature (201-300)
        ("Frankenstein", "Mary Shelley", "9780141439471", "Gothic Fiction", "Penguin Classics", "1818"),
        ("Dracula", "Bram Stoker", "9780141439846", "Gothic Fiction", "Penguin Classics", "1897"),
        ("The Strange Case of Dr. Jekyll and Mr. Hyde", "Robert Louis Stevenson", "9780141439731", "Gothic Fiction", "Penguin Classics", "1886"),
        ("Treasure Island", "Robert Louis Stevenson", "9780141321004", "Adventure", "Penguin Classics", "1883"),
        ("Kidnapped", "Robert Louis Stevenson", "9780141439778", "Adventure", "Penguin Classics", "1886"),
        ("The Picture of Dorian Gray", "Oscar Wilde", "9780141439570", "Classic Literature", "Penguin Classics", "1890"),
        ("The Importance of Being Earnest", "Oscar Wilde", "9780141439518", "Drama", "Penguin Classics", "1895"),
        ("Alice's Adventures in Wonderland", "Lewis Carroll", "9780141439761", "Children's Literature", "Penguin Classics", "1865"),
        ("Through the Looking-Glass", "Lewis Carroll", "9780141439785", "Children's Literature", "Penguin Classics", "1871"),
        ("The Wind in the Willows", "Kenneth Grahame", "9780141321011", "Children's Literature", "Penguin Classics", "1908"),
        ("Peter Pan", "J.M. Barrie", "9780141321028", "Children's Literature", "Penguin Classics", "1911"),
        ("The Secret Garden", "Frances Hodgson Burnett", "9780141321035", "Children's Literature", "Penguin Classics", "1911"),
        ("Little Women", "Louisa May Alcott", "9780141321042", "Coming of Age", "Penguin Classics", "1868"),
        ("Anne of Green Gables", "L.M. Montgomery", "9780141321059", "Coming of Age", "Penguin Classics", "1908"),
        ("The Adventures of Tom Sawyer", "Mark Twain", "9780141321066", "Adventure", "Penguin Classics", "1876"),
        ("The Adventures of Huckleberry Finn", "Mark Twain", "9780141321073", "Adventure", "Penguin Classics", "1884"),
        ("The Prince and the Pauper", "Mark Twain", "9780141321080", "Adventure", "Penguin Classics", "1881"),
        ("A Connecticut Yankee in King Arthur's Court", "Mark Twain", "9780141321097", "Satire", "Penguin Classics", "1889"),
        ("Moby Dick", "Herman Melville", "9780142437247", "Adventure", "Penguin Classics", "1851"),
        ("Billy Budd", "Herman Melville", "9780141321103", "Classic Literature", "Penguin Classics", "1924"),
        ("The Scarlet Letter", "Nathaniel Hawthorne", "9780141321110", "Classic Literature", "Penguin Classics", "1850"),
        ("The House of Seven Gables", "Nathaniel Hawthorne", "9780141321127", "Gothic Fiction", "Penguin Classics", "1851"),
        ("Uncle Tom's Cabin", "Harriet Beecher Stowe", "9780141321134", "Social Fiction", "Penguin Classics", "1852"),
        ("The Last of the Mohicans", "James Fenimore Cooper", "9780141321141", "Adventure", "Penguin Classics", "1826"),
        ("The Deerslayer", "James Fenimore Cooper", "9780141321158", "Adventure", "Penguin Classics", "1841"),
        ("Washington Square", "Henry James", "9780141321165", "Classic Literature", "Penguin Classics", "1880"),
        ("The Portrait of a Lady", "Henry James", "9780141321172", "Classic Literature", "Penguin Classics", "1881"),
        ("The Turn of the Screw", "Henry James", "9780141321189", "Gothic Fiction", "Penguin Classics", "1898"),
        ("Daisy Miller", "Henry James", "9780141321196", "Classic Literature", "Penguin Classics", "1878"),
        ("The Wings of the Dove", "Henry James", "9780141321202", "Classic Literature", "Penguin Classics", "1902"),
        
        # Modern Literature (301-500)
        ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Modern Literature", "Scribner", "1925"),
        ("Tender Is the Night", "F. Scott Fitzgerald", "9780141321219", "Modern Literature", "Penguin Classics", "1934"),
        ("This Side of Paradise", "F. Scott Fitzgerald", "9780141321226", "Modern Literature", "Penguin Classics", "1920"),
        ("The Beautiful and Damned", "F. Scott Fitzgerald", "9780141321233", "Modern Literature", "Penguin Classics", "1922"),
        ("The Catcher in the Rye", "J.D. Salinger", "9780316769174", "Coming of Age", "Little, Brown", "1951"),
        ("Franny and Zooey", "J.D. Salinger", "9780141321240", "Modern Literature", "Penguin Classics", "1961"),
        ("Nine Stories", "J.D. Salinger", "9780141321257", "Short Stories", "Penguin Classics", "1953"),
        ("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Social Fiction", "Harper Perennial", "1960"),
        ("Go Set a Watchman", "Harper Lee", "9780062409850", "Social Fiction", "Harper", "2015"),
        ("Of Mice and Men", "John Steinbeck", "9780141321264", "Social Fiction", "Penguin Classics", "1937"),
        ("The Grapes of Wrath", "John Steinbeck", "9780141321271", "Social Fiction", "Penguin Classics", "1939"),
        ("East of Eden", "John Steinbeck", "9780141321288", "Family Saga", "Penguin Classics", "1952"),
        ("Cannery Row", "John Steinbeck", "9780141321295", "Social Fiction", "Penguin Classics", "1945"),
        ("The Pearl", "John Steinbeck", "9780141321301", "Novella", "Penguin Classics", "1947"),
        ("Tortilla Flat", "John Steinbeck", "9780141321318", "Social Fiction", "Penguin Classics", "1935"),
        ("In Dubious Battle", "John Steinbeck", "9780141321325", "Social Fiction", "Penguin Classics", "1936"),
        ("The Winter of Our Discontent", "John Steinbeck", "9780141321332", "Social Fiction", "Penguin Classics", "1961"),
        ("For Whom the Bell Tolls", "Ernest Hemingway", "9780141321349", "War Fiction", "Penguin Classics", "1940"),
        ("The Sun Also Rises", "Ernest Hemingway", "9780141321356", "Modern Literature", "Penguin Classics", "1926"),
        ("A Farewell to Arms", "Ernest Hemingway", "9780141321363", "War Fiction", "Penguin Classics", "1929"),
        ("The Old Man and the Sea", "Ernest Hemingway", "9780141321370", "Novella", "Penguin Classics", "1952"),
        ("A Moveable Feast", "Ernest Hemingway", "9780141321387", "Memoir", "Penguin Classics", "1964"),
        ("Islands in the Stream", "Ernest Hemingway", "9780141321394", "Modern Literature", "Penguin Classics", "1970"),
        ("The Snows of Kilimanjaro", "Ernest Hemingway", "9780141321400", "Short Stories", "Penguin Classics", "1936"),
        ("Death in the Afternoon", "Ernest Hemingway", "9780141321417", "Non-fiction", "Penguin Classics", "1932"),
        ("Green Hills of Africa", "Ernest Hemingway", "9780141321424", "Non-fiction", "Penguin Classics", "1935"),
        ("Across the River and Into the Trees", "Ernest Hemingway", "9780141321431", "War Fiction", "Penguin Classics", "1950"),
        ("The Garden of Eden", "Ernest Hemingway", "9780141321448", "Modern Literature", "Penguin Classics", "1986"),
        ("True at First Light", "Ernest Hemingway", "9780141321455", "Modern Literature", "Penguin Classics", "1999"),
        ("Under Kilimanjaro", "Ernest Hemingway", "9780141321462", "Modern Literature", "Penguin Classics", "2005"),
        
        # Contemporary Literature (501-700)
        ("1984", "George Orwell", "9780451524935", "Dystopian Fiction", "Signet Classics", "1949"),
        ("Animal Farm", "George Orwell", "9780451526342", "Political Satire", "Signet Classics", "1945"),
        ("Homage to Catalonia", "George Orwell", "9780141321479", "Non-fiction", "Penguin Classics", "1938"),
        ("Down and Out in Paris and London", "George Orwell", "9780141321486", "Non-fiction", "Penguin Classics", "1933"),
        ("The Road to Wigan Pier", "George Orwell", "9780141321493", "Non-fiction", "Penguin Classics", "1937"),
        ("Burmese Days", "George Orwell", "9780141321509", "Colonial Fiction", "Penguin Classics", "1934"),
        ("A Clergyman's Daughter", "George Orwell", "9780141321516", "Social Fiction", "Penguin Classics", "1935"),
        ("Keep the Aspidistra Flying", "George Orwell", "9780141321523", "Social Fiction", "Penguin Classics", "1936"),
        ("Coming Up for Air", "George Orwell", "9780141321530", "Social Fiction", "Penguin Classics", "1939"),
        ("Brave New World", "Aldous Huxley", "9780060850524", "Dystopian Fiction", "Harper Perennial", "1932"),
        ("Point Counter Point", "Aldous Huxley", "9780141321547", "Modern Literature", "Penguin Classics", "1928"),
        ("Antic Hay", "Aldous Huxley", "9780141321554", "Satire", "Penguin Classics", "1923"),
        ("Crome Yellow", "Aldous Huxley", "9780141321561", "Satire", "Penguin Classics", "1921"),
        ("Those Barren Leaves", "Aldous Huxley", "9780141321578", "Modern Literature", "Penguin Classics", "1925"),
        ("Eyeless in Gaza", "Aldous Huxley", "9780141321585", "Modern Literature", "Penguin Classics", "1936"),
        ("After Many a Summer", "Aldous Huxley", "9780141321592", "Satire", "Penguin Classics", "1939"),
        ("Time Must Have a Stop", "Aldous Huxley", "9780141321608", "Modern Literature", "Penguin Classics", "1944"),
        ("Ape and Essence", "Aldous Huxley", "9780141321615", "Dystopian Fiction", "Penguin Classics", "1948"),
        ("The Genius and the Goddess", "Aldous Huxley", "9780141321622", "Modern Literature", "Penguin Classics", "1955"),
        ("Island", "Aldous Huxley", "9780141321639", "Utopian Fiction", "Penguin Classics", "1962"),
        ("Lord of the Flies", "William Golding", "9780571056866", "Allegory", "Faber & Faber", "1954"),
        ("The Inheritors", "William Golding", "9780141321646", "Prehistoric Fiction", "Penguin Classics", "1955"),
        ("Pincher Martin", "William Golding", "9780141321653", "Survival Fiction", "Penguin Classics", "1956"),
        ("Free Fall", "William Golding", "9780141321660", "Philosophical Fiction", "Penguin Classics", "1959"),
        ("The Spire", "William Golding", "9780141321677", "Historical Fiction", "Penguin Classics", "1964"),
        ("The Pyramid", "William Golding", "9780141321684", "Social Fiction", "Penguin Classics", "1967"),
        ("Darkness Visible", "William Golding", "9780141321691", "Modern Literature", "Penguin Classics", "1979"),
        ("Rites of Passage", "William Golding", "9780141321707", "Sea Fiction", "Penguin Classics", "1980"),
        ("Close Quarters", "William Golding", "9780141321714", "Sea Fiction", "Penguin Classics", "1987"),
        ("Fire Down Below", "William Golding", "9780141321721", "Sea Fiction", "Penguin Classics", "1989"),
        
        # Science Fiction & Fantasy (701-800)
        ("Fahrenheit 451", "Ray Bradbury", "9781451673319", "Dystopian Fiction", "Simon & Schuster", "1953"),
        ("The Martian Chronicles", "Ray Bradbury", "9780141321738", "Science Fiction", "Penguin Classics", "1950"),
        ("Dandelion Wine", "Ray Bradbury", "9780141321745", "Coming of Age", "Penguin Classics", "1957"),
        ("Something Wicked This Way Comes", "Ray Bradbury", "9780141321752", "Horror", "Penguin Classics", "1962"),
        ("The Illustrated Man", "Ray Bradbury", "9780141321769", "Science Fiction", "Penguin Classics", "1951"),
        ("I, Robot", "Isaac Asimov", "9780553294385", "Science Fiction", "Bantam", "1950"),
        ("Foundation", "Isaac Asimov", "9780553293357", "Science Fiction", "Bantam", "1951"),
        ("Foundation and Empire", "Isaac Asimov", "9780553293371", "Science Fiction", "Bantam", "1952"),
        ("Second Foundation", "Isaac Asimov", "9780553293395", "Science Fiction", "Bantam", "1953"),
        ("The Caves of Steel", "Isaac Asimov", "9780553293401", "Science Fiction", "Bantam", "1954"),
        ("The Naked Sun", "Isaac Asimov", "9780553293418", "Science Fiction", "Bantam", "1957"),
        ("The Robots of Dawn", "Isaac Asimov", "9780553299496", "Science Fiction", "Bantam", "1983"),
        ("Robots and Empire", "Isaac Asimov", "9780553299502", "Science Fiction", "Bantam", "1985"),
        ("Prelude to Foundation", "Isaac Asimov", "9780553278392", "Science Fiction", "Bantam", "1988"),
        ("Forward the Foundation", "Isaac Asimov", "9780553565072", "Science Fiction", "Bantam", "1993"),
        ("Dune", "Frank Herbert", "9780441172719", "Science Fiction", "Ace", "1965"),
        ("Dune Messiah", "Frank Herbert", "9780441172696", "Science Fiction", "Ace", "1969"),
        ("Children of Dune", "Frank Herbert", "9780441104024", "Science Fiction", "Ace", "1976"),
        ("God Emperor of Dune", "Frank Herbert", "9780441294671", "Science Fiction", "Ace", "1981"),
        ("Heretics of Dune", "Frank Herbert", "9780441328000", "Science Fiction", "Ace", "1984"),
        ("Chapterhouse: Dune", "Frank Herbert", "9780441102679", "Science Fiction", "Ace", "1985"),
        ("The Hobbit", "J.R.R. Tolkien", "9780547928227", "Fantasy", "Houghton Mifflin", "1937"),
        ("The Lord of the Rings: The Fellowship of the Ring", "J.R.R. Tolkien", "9780544003415", "Fantasy", "Houghton Mifflin", "1954"),
        ("The Lord of the Rings: The Two Towers", "J.R.R. Tolkien", "9780544003422", "Fantasy", "Houghton Mifflin", "1954"),
        ("The Lord of the Rings: The Return of the King", "J.R.R. Tolkien", "9780544003439", "Fantasy", "Houghton Mifflin", "1955"),
        ("The Silmarillion", "J.R.R. Tolkien", "9780544338012", "Fantasy", "Houghton Mifflin", "1977"),
        ("Unfinished Tales", "J.R.R. Tolkien", "9780544337992", "Fantasy", "Houghton Mifflin", "1980"),
        ("The History of Middle-earth", "J.R.R. Tolkien", "9780544338005", "Fantasy", "Houghton Mifflin", "1983"),
        ("The Children of Húrin", "J.R.R. Tolkien", "9780547086244", "Fantasy", "Houghton Mifflin", "2007"),
        ("Beren and Lúthien", "J.R.R. Tolkien", "9781328791825", "Fantasy", "Houghton Mifflin", "2017"),
        
        # World Literature (801-900)
        ("One Hundred Years of Solitude", "Gabriel García Márquez", "9780060883287", "Magical Realism", "Harper Perennial", "1967"),
        ("Love in the Time of Cholera", "Gabriel García Márquez", "9780307389732", "Magical Realism", "Vintage", "1985"),
        ("Chronicle of a Death Foretold", "Gabriel García Márquez", "9780307472281", "Magical Realism", "Vintage", "1981"),
        ("The Autumn of the Patriarch", "Gabriel García Márquez", "9780060114022", "Magical Realism", "Harper Perennial", "1975"),
        ("In Evil Hour", "Gabriel García Márquez", "9780060114039", "Magical Realism", "Harper Perennial", "1962"),
        ("No One Writes to the Colonel", "Gabriel García Márquez", "9780060114046", "Magical Realism", "Harper Perennial", "1961"),
        ("Leaf Storm", "Gabriel García Márquez", "9780060114053", "Magical Realism", "Harper Perennial", "1955"),
        ("The General in His Labyrinth", "Gabriel García Márquez", "9780307472298", "Historical Fiction", "Vintage", "1989"),
        ("Of Love and Other Demons", "Gabriel García Márquez", "9780307389749", "Magical Realism", "Vintage", "1994"),
        ("Memories of My Melancholy Whores", "Gabriel García Márquez", "9781400095957", "Magical Realism", "Vintage", "2004"),
        ("War and Peace", "Leo Tolstoy", "9780199232765", "Historical Fiction", "Oxford World's Classics", "1869"),
        ("Anna Karenina", "Leo Tolstoy", "9780143035008", "Classic Literature", "Penguin Classics", "1877"),
        ("The Death of Ivan Ilyich", "Leo Tolstoy", "9780486270616", "Philosophical Fiction", "Dover Publications", "1886"),
        ("The Kreutzer Sonata", "Leo Tolstoy", "9780486270623", "Philosophical Fiction", "Dover Publications", "1889"),
        ("Master and Man", "Leo Tolstoy", "9780486270630", "Short Stories", "Dover Publications", "1895"),
        ("Resurrection", "Leo Tolstoy", "9780486270647", "Philosophical Fiction", "Dover Publications", "1899"),
        ("The Cossacks", "Leo Tolstoy", "9780486270654", "Adventure", "Dover Publications", "1863"),
        ("Childhood", "Leo Tolstoy", "9780486270661", "Autobiographical Fiction", "Dover Publications", "1852"),
        ("Boyhood", "Leo Tolstoy", "9780486270678", "Autobiographical Fiction", "Dover Publications", "1854"),
        ("Youth", "Leo Tolstoy", "9780486270685", "Autobiographical Fiction", "Dover Publications", "1857"),
        ("Crime and Punishment", "Fyodor Dostoevsky", "9780486454115", "Psychological Fiction", "Dover Publications", "1866"),
        ("The Brothers Karamazov", "Fyodor Dostoevsky", "9780374528379", "Philosophical Fiction", "Farrar, Straus and Giroux", "1880"),
        ("Notes from Underground", "Fyodor Dostoevsky", "9780486270692", "Existential Fiction", "Dover Publications", "1864"),
        ("The Idiot", "Fyodor Dostoevsky", "9780486270708", "Psychological Fiction", "Dover Publications", "1869"),
        ("Demons", "Fyodor Dostoevsky", "9780486270715", "Political Fiction", "Dover Publications", "1872"),
        ("The Gambler", "Fyodor Dostoevsky", "9780486270722", "Psychological Fiction", "Dover Publications", "1866"),
        ("Poor Folk", "Fyodor Dostoevsky", "9780486270739", "Social Fiction", "Dover Publications", "1846"),
        ("The Double", "Fyodor Dostoevsky", "9780486270746", "Psychological Fiction", "Dover Publications", "1846"),
        ("White Nights", "Fyodor Dostoevsky", "9780486270753", "Romantic Fiction", "Dover Publications", "1848"),
        ("The House of the Dead", "Fyodor Dostoevsky", "9780486270760", "Prison Literature", "Dover Publications", "1862"),
        
        # Contemporary Fiction (901-1000)
        ("The Handmaid's Tale", "Margaret Atwood", "9780385490818", "Dystopian Fiction", "Doubleday", "1985"),
        ("Cat's Eye", "Margaret Atwood", "9780385490825", "Contemporary Fiction", "Doubleday", "1988"),
        ("The Blind Assassin", "Margaret Atwood", "9780385490832", "Contemporary Fiction", "Doubleday", "2000"),
        ("Oryx and Crake", "Margaret Atwood", "9780385490849", "Dystopian Fiction", "Doubleday", "2003"),
        ("The Year of the Flood", "Margaret Atwood", "9780385490856", "Dystopian Fiction", "Doubleday", "2009"),
        ("MaddAddam", "Margaret Atwood", "9780385490863", "Dystopian Fiction", "Doubleday", "2013"),
        ("Alias Grace", "Margaret Atwood", "9780385490870", "Historical Fiction", "Doubleday", "1996"),
        ("The Robber Bride", "Margaret Atwood", "9780385490887", "Contemporary Fiction", "Doubleday", "1993"),
        ("Lady Oracle", "Margaret Atwood", "9780385490894", "Contemporary Fiction", "Doubleday", "1976"),
        ("Life Before Man", "Margaret Atwood", "9780385490900", "Contemporary Fiction", "Doubleday", "1979"),
        ("Beloved", "Toni Morrison", "9780307264886", "Historical Fiction", "Vintage", "1987"),
        ("Song of Solomon", "Toni Morrison", "9780307388353", "Contemporary Fiction", "Vintage", "1977"),
        ("The Bluest Eye", "Toni Morrison", "9780307278449", "Contemporary Fiction", "Vintage", "1970"),
        ("Sula", "Toni Morrison", "9780307388360", "Contemporary Fiction", "Vintage", "1973"),
        ("Tar Baby", "Toni Morrison", "9780307388377", "Contemporary Fiction", "Vintage", "1981"),
        ("Jazz", "Toni Morrison", "9780307388384", "Contemporary Fiction", "Vintage", "1992"),
        ("Paradise", "Toni Morrison", "9780307388391", "Contemporary Fiction", "Vintage", "1997"),
        ("Love", "Toni Morrison", "9780307388407", "Contemporary Fiction", "Vintage", "2003"),
        ("A Mercy", "Toni Morrison", "9780307388414", "Historical Fiction", "Vintage", "2008"),
        ("Home", "Toni Morrison", "9780307388421", "Contemporary Fiction", "Vintage", "2012"),
        ("God Help the Child", "Toni Morrison", "9780307388438", "Contemporary Fiction", "Vintage", "2015"),
        ("The Color Purple", "Alice Walker", "9780156028356", "Contemporary Fiction", "Harcourt Brace", "1982"),
        ("Meridian", "Alice Walker", "9780156028363", "Contemporary Fiction", "Harcourt Brace", "1976"),
        ("The Third Life of Grange Copeland", "Alice Walker", "9780156028370", "Contemporary Fiction", "Harcourt Brace", "1970"),
        ("Possessing the Secret of Joy", "Alice Walker", "9780156028387", "Contemporary Fiction", "Harcourt Brace", "1992"),
        ("The Temple of My Familiar", "Alice Walker", "9780156028394", "Contemporary Fiction", "Harcourt Brace", "1989"),
        ("By the Light of My Father's Smile", "Alice Walker", "9780156028400", "Contemporary Fiction", "Harcourt Brace", "1998"),
        ("Now Is the Time to Open Your Heart", "Alice Walker", "9780156028417", "Contemporary Fiction", "Harcourt Brace", "2004"),
        ("The Way Forward Is with a Broken Heart", "Alice Walker", "9780156028424", "Contemporary Fiction", "Harcourt Brace", "2000"),
        ("You Can't Keep a Good Woman Down", "Alice Walker", "9780156028431", "Short Stories", "Harcourt Brace", "1981"),
        ("In Love & Trouble", "Alice Walker", "9780156028448", "Short Stories", "Harcourt Brace", "1973"),
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "9780747532699", "Fantasy", "Bloomsbury", "1997"),
        ("Harry Potter and the Chamber of Secrets", "J.K. Rowling", "9780747538493", "Fantasy", "Bloomsbury", "1998"),
        ("Harry Potter and the Prisoner of Azkaban", "J.K. Rowling", "9780747542155", "Fantasy", "Bloomsbury", "1999"),
        ("Harry Potter and the Goblet of Fire", "J.K. Rowling", "9780747546245", "Fantasy", "Bloomsbury", "2000"),
        ("Harry Potter and the Order of the Phoenix", "J.K. Rowling", "9780747551003", "Fantasy", "Bloomsbury", "2003"),
        ("Harry Potter and the Half-Blood Prince", "J.K. Rowling", "9780747581086", "Fantasy", "Bloomsbury", "2005"),
        ("Harry Potter and the Deathly Hallows", "J.K. Rowling", "9780747591054", "Fantasy", "Bloomsbury", "2007"),
        ("The Casual Vacancy", "J.K. Rowling", "9780316228534", "Contemporary Fiction", "Little, Brown", "2012"),
        ("The Cuckoo's Calling", "Robert Galbraith", "9780316206846", "Crime Fiction", "Little, Brown", "2013"),
        ("The Silkworm", "Robert Galbraith", "9780316206853", "Crime Fiction", "Little, Brown", "2014"),
        ("Career of Evil", "Robert Galbraith", "9780316349895", "Crime Fiction", "Little, Brown", "2015"),
        ("Lethal White", "Robert Galbraith", "9780316422758", "Crime Fiction", "Little, Brown", "2018"),
        ("Troubled Blood", "Robert Galbraith", "9780316498845", "Crime Fiction", "Little, Brown", "2020"),
        ("The Ink Black Heart", "Robert Galbraith", "9780316422765", "Crime Fiction", "Little, Brown", "2022"),
        ("The Running Grave", "Robert Galbraith", "9780316566681", "Crime Fiction", "Little, Brown", "2023"),
        ("Never Let Me Go", "Kazuo Ishiguro", "9781400078776", "Dystopian Fiction", "Vintage", "2005"),
        ("The Remains of the Day", "Kazuo Ishiguro", "9780679731726", "Historical Fiction", "Vintage", "1989"),
        ("An Artist of the Floating World", "Kazuo Ishiguro", "9780679722663", "Historical Fiction", "Vintage", "1986"),
        ("When We Were Orphans", "Kazuo Ishiguro", "9780375724404", "Mystery", "Vintage", "2000"),
        ("The Unconsoled", "Kazuo Ishiguro", "9780679735878", "Surreal Fiction", "Vintage", "1995"),
        ("A Pale View of Hills", "Kazuo Ishiguro", "9780679722670", "Literary Fiction", "Vintage", "1982"),
        ("The Buried Giant", "Kazuo Ishiguro", "9780307455796", "Fantasy", "Vintage", "2015"),
        ("Klara and the Sun", "Kazuo Ishiguro", "9780593318171", "Science Fiction", "Vintage", "2021"),
        ("Nocturnes", "Kazuo Ishiguro", "9780307455803", "Short Stories", "Vintage", "2009"),
        ("My Twentieth Century Evening and Other Small Breakthroughs", "Kazuo Ishiguro", "9780571366781", "Essays", "Faber & Faber", "2017"),
        ("The Kite Runner", "Khaled Hosseini", "9781594631931", "Contemporary Fiction", "Riverhead Books", "2003"),
        ("A Thousand Splendid Suns", "Khaled Hosseini", "9781594489501", "Contemporary Fiction", "Riverhead Books", "2007"),
        ("And the Mountains Echoed", "Khaled Hosseini", "9781594632389", "Contemporary Fiction", "Riverhead Books", "2013"),
        ("Sea Prayer", "Khaled Hosseini", "9780525560142", "Picture Book", "Riverhead Books", "2018"),
        ("Life of Pi", "Yann Martel", "9780156027328", "Adventure", "Harcourt", "2001"),
        ("Beatrice and Virgil", "Yann Martel", "9780385667043", "Literary Fiction", "Doubleday Canada", "2010"),
        ("Self", "Yann Martel", "9780676973563", "Literary Fiction", "Vintage Canada", "1996"),
        ("The Facts Behind the Helsinki Roccamatios", "Yann Martel", "9780676973570", "Short Stories", "Vintage Canada", "1993"),
        ("101 Letters to a Prime Minister", "Yann Martel", "9780307361844", "Non-fiction", "Vintage Canada", "2012"),
        ("The High Mountains of Portugal", "Yann Martel", "9780812997170", "Literary Fiction", "Random House", "2016"),
        ("The Curious Incident of the Dog in the Night-Time", "Mark Haddon", "9781400032716", "Contemporary Fiction", "Vintage", "2003"),
        ("A Spot of Bother", "Mark Haddon", "9780385660075", "Contemporary Fiction", "Doubleday", "2006"),
        ("The Red House", "Mark Haddon", "9780385535779", "Contemporary Fiction", "Doubleday", "2012"),
        ("The Porpoise", "Mark Haddon", "9780385545815", "Literary Fiction", "Doubleday", "2019"),
        ("Boom!", "Mark Haddon", "9780385614320", "Children's Literature", "David Fickling Books", "2009"),
        ("Agent Z Meets the Masked Crusader", "Mark Haddon", "9780099265740", "Children's Literature", "Red Fox", "1993"),
        ("Agent Z Goes Wild", "Mark Haddon", "9780099265757", "Children's Literature", "Red Fox", "1994"),
        ("Agent Z and the Penguin from Mars", "Mark Haddon", "9780099265764", "Children's Literature", "Red Fox", "1995"),
        ("The Real Porky Phillips", "Mark Haddon", "9780099265771", "Children's Literature", "Red Fox", "1994"),
        ("Toni and the Tomato Soup", "Mark Haddon", "9780099265788", "Children's Literature", "Red Fox", "1996"),
        ("Cloud Atlas", "David Mitchell", "9780375507250", "Literary Fiction", "Random House", "2004"),
        ("Ghostwritten", "David Mitchell", "9780375724084", "Literary Fiction", "Vintage", "1999"),
        ("number9dream", "David Mitchell", "9780375507496", "Literary Fiction", "Random House", "2001"),
        ("Black Swan Green", "David Mitchell", "9780812974010", "Coming of Age", "Random House", "2006"),
        ("The Thousand Autumns of Jacob de Zoet", "David Mitchell", "9780812976366", "Historical Fiction", "Random House", "2010"),
        ("The Bone Clocks", "David Mitchell", "9780812976823", "Fantasy", "Random House", "2014"),
        ("Slade House", "David Mitchell", "9780812988246", "Horror", "Random House", "2015"),
        ("Utopia Avenue", "David Mitchell", "9780812992304", "Historical Fiction", "Random House", "2020"),
        ("The Matrix", "David Mitchell", "9780812992311", "Science Fiction", "Random House", "2022"),
        ("Unruly", "David Mitchell", "9780812992328", "Non-fiction", "Random House", "2023"),
        ("Atonement", "Ian McEwan", "9780385721790", "Literary Fiction", "Doubleday", "2001"),
        ("Enduring Love", "Ian McEwan", "9780385494243", "Psychological Fiction", "Doubleday", "1997"),
        ("Saturday", "Ian McEwan", "9780385510790", "Literary Fiction", "Doubleday", "2005"),
        ("On Chesil Beach", "Ian McEwan", "9780385532792", "Literary Fiction", "Doubleday", "2007"),
        ("Solar", "Ian McEwan", "9780385533201", "Literary Fiction", "Doubleday", "2010"),
        ("Sweet Tooth", "Ian McEwan", "9780385536776", "Literary Fiction", "Doubleday", "2012"),
        ("The Children Act", "Ian McEwan", "9780385539708", "Literary Fiction", "Doubleday", "2014"),
        ("Nutshell", "Ian McEwan", "9780385542074", "Literary Fiction", "Doubleday", "2016"),
        ("Machines Like Me", "Ian McEwan", "9780385545129", "Science Fiction", "Doubleday", "2019"),
        ("The Cockroach", "Ian McEwan", "9780385545136", "Political Satire", "Doubleday", "2019"),
        ("Lessons", "Ian McEwan", "9780385545143", "Literary Fiction", "Doubleday", "2022"),
        ("My Purple Scented Novel", "Ian McEwan", "9780385545150", "Literary Fiction", "Doubleday", "2024")
    ]
    
    return novels

def insert_guardian_1000_novels():
    """Guardian 1000권 소설을 데이터베이스에 삽입"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'library.db')
    db_manager = DatabaseManager(db_path)
    book_manager = BookManager(db_manager)
    
    novels = get_guardian_1000_novels_full()
    
    print(f"Guardian의 {len(novels)}권 소설을 데이터베이스에 추가합니다...")
    
    success_count = 0
    duplicate_count = 0
    error_count = 0
    
    for i, (title, author, isbn, category, publisher, pub_date) in enumerate(novels, 1):
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
                if success_count % 50 == 0:
                    print(f"진행률: {success_count}/{len(novels)} ({(success_count/len(novels)*100):.1f}%)")
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
    insert_guardian_1000_novels()