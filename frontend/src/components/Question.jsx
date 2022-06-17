import React, { Component } from 'react';
import ReactStars from 'react-rating-stars-component';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }
  ratingChanged(newRating){
    console.log(newRating)
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className='Question-holder'>
        <div className='Question'>{question}</div>
        <div className='Question-status'>
          <img
            className='category'
            alt={`${category.toLowerCase()}`}
            src={`${category.toLowerCase()}.svg`}
          />
          <div className='difficulty'>Difficulty: {difficulty}</div>
          <ReactStars
            count={5}
            onChange={this.ratingChanged}
            size={24}
            isHalf={true}
            emptyIcon={<i className="fa fa-star"></i>}
            halfIcon={<i className="fa fa-star-half-alt"></i>}
            fullIcon={<i className="fa fa-star"></i>}
            activeColor="#ffd700"/>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
        <div
          className='show-answer button'
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
        <div className='answer-holder'>
          <span
            style={{
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
