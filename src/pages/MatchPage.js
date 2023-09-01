import React from 'react'
import TopApp from '../components/TopApp'

function MatchPage() {
  return (
    <>
    <div className="container vh-100">
      <div className="page_element_container h-100 d-flex flex-column justify-content-between">
        <div className="top_element_container">
          <div className="top_content_container mb-5">
            <TopApp to="/matches" message="Matches" />
          </div>
        </div>
      </div>
    </div>
    </>
  )
}

export default MatchPage