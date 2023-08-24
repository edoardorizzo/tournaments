import React from 'react'
import Button from './Button'


function StartMatchComp() {
  return (
    <div className='background_start_match'>
        <h3>Start your first match!</h3>
        <Button to="/tournament" text="Start torunament"></Button>
    </div>
  )
}

export default StartMatchComp