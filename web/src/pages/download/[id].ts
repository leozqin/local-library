import type { APIRoute } from "astro"

export const GET: APIRoute = async ({params}) => {

    const apiEndpoint: string = import.meta.env.API_BASE_URL
        ? import.meta.env.API_BASE_URL
        : "http://api";

    const response = await fetch(`${apiEndpoint}/download/${params.id}`);

    return response;
}