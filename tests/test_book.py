from app import schemas
import pytest

def test_all_record(authorized_client):
    res = authorized_client.get("/book/")
    def validate(book):
        return schemas.RecordOut(**book)
    book_map=map(validate,res.json())
    book_list=list(book_map)
    # assert len(res.json()) == len(test_tasks)
    assert res.status_code == 200

def test_unauthorized_user_get_all_record(client):
    res=client.get("/book/",)
    assert res.status_code == 401

def test_unauthorized_user_get_one_record(client,test_books):
    res=client.get(f"/book/{test_books[0].id}")
    assert res.status_code == 401

def test_get_one_record_not_exists(authorized_client):
    res=authorized_client.get(f"/book/{88888}")
    assert res.status_code == 404

def test_get_one_record(authorized_client,test_books):
    res=authorized_client.get(f"/book/{test_books[0].id}")
    assert res.status_code == 200

@pytest.mark.parametrize("title, author",[
    ("Book 1","Author 1"),
    ("Book 2","Author 2"),
    ("Book 3","Author 3"),
    ("Book 4","Author 4")
])
def test_create_record(authorized_client,title,author):
    res=authorized_client.post("/book/",json={"title":title,"author":author})
    create_record=schemas.RecordOut(**res.json())
    assert res.status_code == 200
    assert create_record.title == title
    assert create_record.author == author

def test_unauthorized_user_create_record(client):
    res=client.post("/book/",json={"title":"Book 1","author":"Author1"})
    assert res.status_code == 401

def test_unauthorized_user_delete_record(client,test_books):
    res=client.delete(f"/book/{test_books[0].id}")
    assert res.status_code == 401

def test_delete_record_success(authorized_client,test_books):
    res=authorized_client.delete(f"/book/{test_books[0].id}")
    assert res.status_code == 200

def test_delete_record_not_exist(authorized_client):
    res=authorized_client.delete(f"/book/{8888}")
    assert res.status_code == 404

def test_delete_other_user_record(authorized_client,test_books):
    res=authorized_client.delete(f"/book/{test_books[3].id}")
    assert res.status_code == 403

def test_update_record(authorized_client,test_books):
    data={
        "title":"Utitle",
        "author":"Uauthor",
        "id":test_books[0].id
    }
    book_id=test_books[0].id
    res=authorized_client.put(f"/book/{book_id}",json=data)
    assert res.status_code == 200
    updated_record=schemas.RecordBase(**res.json())
    assert updated_record.title == "Utitle"
    assert updated_record.author == "Uauthor"

def test_update_other_user_record(authorized_client,test_books):
    data={
        "title":"Utitle",
        "author":"Uauthor",
        "id":test_books[3].id
    }
    book_id=test_books[3].id
    res=authorized_client.put(f"/book/{book_id}",json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_record(client,test_books):
    res=client.put(f"/book/{test_books[0].id}")
    assert res.status_code == 401

def test_update_record_not_exist(authorized_client,test_books):
    data={
        "title":"Utitle",
        "author":"Uauthor",
        "id":test_books[3].id
    }
    res=authorized_client.put(f"/book/8888",json=data)
    assert res.status_code == 404