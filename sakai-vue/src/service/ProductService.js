export class ProductService {
    getProducts() {
        const token = localStorage.getItem('token');
        return fetch('/api/repos/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
            .then((res) => res.json())
            .then((d) => {
                console.log(d);
                return d;
            });
    }
    getProfile() {
        const token = localStorage.getItem('token');
        return fetch('/api/profile/', {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
            .then((res) => res.json())
            .then((d) => {
                console.log(d);
                return d;
            });
    }
}
