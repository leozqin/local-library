
export async function GET({ params }) {
    const id = params.id;
    const response = await fetch(`http://localhost:8000/download/${id}`);
    
    return response
};
