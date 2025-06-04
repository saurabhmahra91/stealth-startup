// JustificationFooter.jsx (example)
export default function JustificationFooter({ justification, followUp }) {
    return (
        <footer className="justification-footer">
            Follow Up: {followUp && <p>{followUp}</p>}
            {/* Justification: {justification && <p>{justification}</p>} */}
        </footer>
    )
}
