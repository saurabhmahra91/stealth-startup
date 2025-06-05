export default function JustificationFooter({ justification, followUp, loading }) {
    return (
        <footer className="justification-footer">
            {loading ? (
                <p className="footer-loader">Loading...</p>
            ) : (
                <>
                    {followUp && <p>Follow Up: {followUp}</p>}
                    {justification && <p>Justification: {justification}</p>}
                </>
            )}
        </footer>
    )
}