from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
def get_data():
    return {"data": "This is your fetched data"}

@router.post("/data")
def create_data():
    return {"message": "Data created successfully"}

@router.put("/data/{id}")
def update_data(id: int):
    return {"message": f"Data with ID {id} updated successfully"}

@router.delete("/data/{id}")
def delete_data(id: int):
    return {"message": f"Data with ID {id} deleted successfully"}