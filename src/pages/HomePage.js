import React from 'react'
import Header from '../components/Header'
import StartMatchComp from '../components/StartMatchComp'

function HomePage() {
  return (
    <div className='container'>
        <Header></Header>
        <StartMatchComp></StartMatchComp>
    </div>
  )
}

export default HomePage