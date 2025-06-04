import React, { useState } from 'react'

export default function SearchBar({ onSearch, onFlush }) {
    const [query, setQuery] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (query.trim()) {
            onSearch(query)
            setQuery('')
        }
    }

    return (
        <div className="search-bar">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Search for a product..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit">Search</button>
                <button type="button" onClick={onFlush} style={{ marginLeft: '10px' }}>
                    Flush Session
                </button>
            </form>
        </div>
    )
}
