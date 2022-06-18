import React, { Component } from 'react';
import ReactStars from 'react-rating-stars-component';
import '../stylesheets/Question.css';
import $ from 'jquery';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
      rating: null
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  /**Listen to rating changes and update on the database */
  ratingChanged = (newRating) => {
    const question_id = this.props.id;
    $.ajax({
      /**Add: update rating */
      url: `/questions/${question_id}`,
      type: 'PATCH',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ rating: newRating }),
      xhrFields: {
          withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        const question = result['question']
        this.setState({
          rating: question['rating']
        });
        return;
      },
      error: (error) => {
        alert('Question rating cannot be updated')
        return;
      },
    });
  }

  render() {
    const { question, answer, category, difficulty, rating } = this.props;
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
            activeColor="#ffd700"
            value={this.state.rating ? this.state.rating :rating}/>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}/>
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
