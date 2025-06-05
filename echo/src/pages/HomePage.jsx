import React, { useState, useEffect } from 'react'
import SearchBar from '../components/SearchBar'
import ProductList from '../components/ProductList'
import JustificationFooter from '../components/JustificationFooter'

const API_URL = import.meta.env.VITE_API_URL;
console.log("backend api base = ", API_URL)
// const API_URL = 'http://localhost:8000' // Ensure this matches your backend

export default function HomePage() {
    const [products, setProducts] = useState([])
    const [justification, setJustification] = useState('')
    const [followUp, setFollowUp] = useState('')
    const [userId] = useState(() => {
        const saved = localStorage.getItem('user_id')
        if (saved) return saved
        const newId = crypto.randomUUID()
        localStorage.setItem('user_id', newId)
        return newId
    })

    const [loading, setLoading] = useState(false)

    const handleSearch = async (query) => {
        setLoading(true)
        const res = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, user_input: query }),
        })
        const data = await res.json()
        setProducts(data.products)
        setJustification(data.justification)
        setFollowUp(data.follow_up)
        setLoading(false)
    }

    const handleFlush = async () => {
        await fetch(`${API_URL}/flush?user_id=${userId}`, { method: 'POST' })
        setProducts([])
        setJustification('')
        setFollowUp('')
    }

    return (
        <div className="home-page">
            <SearchBar onSearch={handleSearch} onFlush={handleFlush} />
            <ProductList products={products} />
            {(loading || justification || followUp) && (
                <JustificationFooter
                    loading={loading}
                    justification={justification}
                    followUp={followUp}
                />
            )}

        </div>
    )
}


