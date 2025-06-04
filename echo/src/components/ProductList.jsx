import React from 'react'

export default function ProductList({ products }) {
    if (!products.length) return <p>No products found yet.</p>

    return (
        <div className="product-list">
            {products.map((p) => (
                <div key={p.product_id} className="product-card">
                    <h3 className="product-name">{p.name}</h3>
                    <p className="product-description">{p.description}</p>
                    <p className="product-price"><strong>Price:</strong> ${p.usd_price}</p>
                    <p className="product-tags"><strong>Tags:</strong> {p.tags}</p>
                </div>
            ))}
        </div>
    )
}
