document.addEventListener("DOMContentLoaded", () => {
    console.log("yaha tak phauvhe");
    

    // Update progress bars
    document.getElementById("attempted-progress-bar").style.width = `${(data.attempted / 75) * 100}%`;
    document.getElementById("correct-progress-bar").style.width = `${(data.correct / 75) * 100}%`;
    document.getElementById("incorrect-progress-bar").style.width = `${(data.incorrect / 75) * 100}%`;
    document.getElementById("skipped-progress-bar").style.width = `${(data.skipped / 75) * 100}%`;
    document.getElementById("completed-progress-bar").style.width = `${data.completed_percentage}%`;
    document.getElementById("accuracy-progress-bar").style.width = `${data.accuracy}%`;
    
//     /// Update subject-wise progress bars

// // Physics
// document.getElementById("physics-attempted-progress-bar").style.width = `${(data.subject_data.Physics.attempted / 25) * 100}%`;
// document.getElementById("physics-correct-progress-bar").style.width = `${(data.subject_data.Physics.correct / data.subject_data.Physics.attempted) * 100}%`;
// document.getElementById("physics-incorrect-progress-bar").style.width = `${(data.subject_data.Physics.incorrect / data.subject_data.Physics.attempted) * 100}%`;
// document.getElementById("physics-accuracy-progress-bar").style.width = `${data.subject_data.Physics.accuracy}%`;

// // Chemistry
// document.getElementById("chemistry-attempted-progress-bar").style.width = `${(data.subject_data.Chemistry.attempted / 25)  * 100}%`;
// document.getElementById("chemistry-correct-progress-bar").style.width = `${(data.subject_data.Chemistry.correct / data.subject_data.Chemistry.attempted) * 100}%`;
// document.getElementById("chemistry-incorrect-progress-bar").style.width = `${(data.subject_data.Chemistry.incorrect / data.subject_data.Chemistry.attempted) * 100}%`;
// document.getElementById("chemistry-accuracy-progress-bar").style.width = `${data.subject_data.Chemistry.accuracy}%`;

// // Mathematics
// document.getElementById("maths-attempted-progress-bar").style.width = `${(data.subject_data.Mathematics.attempted / 25) * 100}%`;
// document.getElementById("maths-correct-progress-bar").style.width = `${(data.subject_data.Mathematics.correct / data.subject_data.Mathematics.attempted) * 100}%`;
// document.getElementById("maths-incorrect-progress-bar").style.width = `${(data.subject_data.Mathematics.incorrect / data.subject_data.Mathematics.attempted) * 100}%`;
// document.getElementById("maths-accuracy-progress-bar").style.width = `${data.subject_data.Mathematics.accuracy}%`;

//    //circular progress 
   
//    // Helper function to update circular progress
// function updateCircularProgress(elementId, percentage) {
// const progressElement = document.getElementById(elementId);
// if (progressElement) {
// progressElement.style.background = `conic-gradient(#6366f1 ${percentage * 3.6}deg, #e5e7eb 0deg)`;
// }
// }

// // Update circular progress for Physics, Chemistry, Mathematics
// updateCircularProgress("physics-progress", data.subject_data.Physics.score);
// updateCircularProgress("chemistry-progress", data.subject_data.Chemistry.score);
// updateCircularProgress("maths-progress", data.subject_data.Mathematics.score);


    //chem
    
    // console.log(q);
  
    //     const numberContainer = document.getElementById('number-container');
    //     const dynamicContainer = document.getElementById('dynamic-container');
    //     const correctAnswerKey =answer; // Make sure this is correctly defined
    //     //const q = [.../* Your question data array */ ]; // Make sure this is correctly defined
    
    //     // Create number buttons with color coding
    //     function displayNumbers() {
    //         for (let i = 0; i < q.length; i++) { // Iterate through the question array
    //             const questionData = q[i];
    //             const numberDiv = document.createElement('div');
    //             numberDiv.textContent = i + 1;
    //             numberDiv.classList.add('cursor-pointer', 'flex', 'items-center', 'justify-center');
    
    //             // Apply color based on status
    //             if (questionData.status === 'Answered') {
    //                 const chosenOption = questionData.chosen_option;
    //                 const correctOption = correctAnswerKey[questionData.question_id];
    
    //                 if (chosenOption && correctOption && questionData.option_ids[Number(chosenOption)-1] === correctOption.toString()) {
    //                     numberDiv.classList.add('correct');
    //                 } else if (chosenOption && correctOption && questionData.option_ids[Number(chosenOption)-1] !== correctOption.toString()) {
    //                     numberDiv.classList.add('incorrect');
    //                 } else if (questionData.given_answer && correctAnswerKey[questionData.question_id] && questionData.given_answer.toString().trim() === correctAnswerKey[questionData.question_id].toString().trim()) {
    //                     numberDiv.classList.add('correct');
    //                 } else if (questionData.given_answer && correctAnswerKey[questionData.question_id] && questionData.given_answer.toString().trim() !== correctAnswerKey[questionData.question_id].toString().trim()) {
    //                     numberDiv.classList.add('incorrect');
    //                 }
    
    //             } else if (questionData.status === 'Not Answered' || questionData.status === 'Skipped') {
    //                 numberDiv.classList.add('skipped');
    //             }
    
    //             numberDiv.addEventListener('click', () => {
    //                 // Remove active class from previous
    //                 const activeNumber = document.querySelector('.active-number');
    //                 if (activeNumber) {
    //                     activeNumber.classList.remove('active-number');
    //                 }
    //                 numberDiv.classList.add('active-number');
    
    //                 // Clear old question display
    //                 dynamicContainer.innerHTML = '';
    
    //                 // Add new question display
    //                 const questionElement = createQuestionDisplay(questionData, correctAnswerKey);
    //                 dynamicContainer.appendChild(questionElement);
    //             });
    //             numberContainer.appendChild(numberDiv);
    //         }
    //     }



    //     function getVideoSolution(questionId) {
    //         // In a real scenario, you would fetch the video URL based on the questionId
    //         // from your backend or a data source.
    //         // For example:
    //         // return fetch(`/api/videos/${questionId}`).then(res => res.json()).then(data => data.url);
    //         // Or, if you have a local map:
    //         const videoMap = {
    //             /* 'questionId1': 'url1.mp4', */
    //             // Add your question ID to video URL mappings here
    //         };
    //         //return videoMap[questionId];
    //         return 'static/solution.mp4';
    //     }
    
    //     function createQuestionDisplay(question, correctAnswers) {
    //         const mainContainer = document.createElement('div');
    //         mainContainer.innerHTML = `<h2>Question ${q.indexOf(question) + 1}</h2>`;
    
    //         // Question Image
    //         if (question.question_image_url && question.question_image_url !== "None") {
    //             const img = document.createElement('img');
    //             img.src = "https://cdn3.digialm.com" + question.question_image_url;
    //             img.alt = 'Question Image';
    //             mainContainer.appendChild(img);
    //         }
    
    //         if (question.question_type === "SA") {
    //             // Subjective/Numerical Answer
    //             mainContainer.innerHTML += `<div><strong>Your Answer:</strong> ${question.given_answer !== '--' ? question.given_answer : '<span class="skipped-answer">Skipped</span>'}</div>`;
    //             const correctAnswerSA = correctAnswers[question.question_id];
    //             if (correctAnswerSA) {
    //                 mainContainer.innerHTML += `<div><strong>Correct Answer:</strong> ${correctAnswerSA}</div>`;
    //             }
    //         } else {
    //             // MCQ
    //             if (question.option_image_urls && question.option_image_urls[0] !== "None") {
    //                 const optionsContainer = document.createElement('div');
    //                 optionsContainer.classList.add('options-container');
    
    //                 question.option_image_urls.forEach((optionUrl, index) => {
    //                     if (optionUrl) {
    //                         const optionRow = document.createElement('div');
    //                         optionRow.classList.add('option-row');
    //                         optionRow.innerHTML = `<span class="option-label">${String.fromCharCode(65 + index)}.</span><img src="https://cdn3.digialm.com${optionUrl}" alt="Option ${String.fromCharCode(65 + index)}">`;
    //                         optionsContainer.appendChild(optionRow);
    //                     }
    //                 });
    //                 mainContainer.appendChild(optionsContainer);
    //             }
    
    //             const yourAnswerMCQ = question.chosen_option !== '--' ? String.fromCharCode(64 + parseInt(question.chosen_option)) : '<span class="skipped-answer">Skipped</span>';
    //             const correctAnswerMCQ = correctAnswers[question.question_id] ? String.fromCharCode(65 + parseInt(question.option_ids.indexOf(correctAnswers[question.question_id])  )) : 'Not Available';
    
    //             mainContainer.innerHTML += `<div class="your-answer"><strong>Your Answer:</strong> ${yourAnswerMCQ}</div>`;
    //             mainContainer.innerHTML += `<div class="correct-answer"><strong>Correct Answer:</strong> ${correctAnswerMCQ}</div>`;
    //         }

    //         // Video Solution
    //         const videoUrl = getVideoSolution(question.question_id); // Function to get video URL
    //         if (videoUrl) {
    //             const videoContainer = document.createElement('div');
    //             videoContainer.style.marginTop = '20px';
    //             videoContainer.innerHTML = `
    //                 <h3>Solution Video</h3>
    //                 <video width="100%" controls>
    //                     <source src="${videoUrl}" type="video/mp4">
    //                     Your browser does not support the video tag.
    //                 </video>
    //             `;
    //             mainContainer.appendChild(videoContainer);
    //         }
        

    
    //         return mainContainer;
    //     }
    
    //     // Initial call
    //     if (q && q.length > 0 && correctAnswerKey) {
    //         displayNumbers();
    //         // Display the first question by default
    //         const firstQuestionData = q[0];
    //         if (firstQuestionData) {
    //             const firstNumberDiv = numberContainer.firstChild;
    //             if (firstNumberDiv) {
    //                 firstNumberDiv.classList.add('active-number');
    //             }
    //             dynamicContainer.appendChild(createQuestionDisplay(firstQuestionData, correctAnswerKey));
    //         }
    //     }
   
    


  
const numberContainer = document.getElementById('number-container');
const dynamicContainer = document.getElementById('dynamic-container');
const correctAnswerKey = answer;  // image path or ID-based correct answers
const q = questionss;              // question array from backend

function displayNumbers() {
    for (let i = 0; i < q.length; i++) {
        const questionData = q[i];
        const numberDiv = document.createElement('div');
        numberDiv.textContent = i + 1;
        numberDiv.classList.add('cursor-pointer', 'flex', 'items-center', 'justify-center', 'w-8', 'h-8', 'rounded', 'text-white', 'font-bold');

        // Color code based on evaluation
        if (questionData.status === 'Answered') {
            if (questionData.status_correct) {
                numberDiv.classList.add('bg-green-500');  // correct
            } else {
                numberDiv.classList.add('bg-red-500');    // incorrect
            }
        } else {
            numberDiv.classList.add('bg-gray-400');        // skipped
        }

        numberDiv.addEventListener('click', () => {
            document.querySelectorAll('.active-number').forEach(el => el.classList.remove('active-number'));
            numberDiv.classList.add('active-number');
            dynamicContainer.innerHTML = '';
            dynamicContainer.appendChild(createQuestionDisplay(questionData));
        });

        numberContainer.appendChild(numberDiv);
    }
}

function getVideoSolution(questionId) {
    // Customize this per your backend logic if needed
    return 'static/solution.mp4';
}

function createQuestionDisplay(question) {
    const mainContainer = document.createElement('div');
    mainContainer.innerHTML = `<h2 class="text-xl font-semibold mb-2">Question ${q.indexOf(question) + 1}</h2>`;

    if (question.question_image_url && question.question_image_url !== "None") {
        const img = document.createElement('img');
        img.src = "https://cdn3.digialm.com" + question.question_image_url;
        img.alt = "Question";
        img.className = "w-full max-w-xl mb-4";
        mainContainer.appendChild(img);
    }

    // Show options if present
    if (question.option_image_urls && question.option_image_urls.length > 0) {
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'grid grid-cols-2 gap-4';

        question.option_image_urls.forEach((url, index) => {
            if (url && url !== "None") {
                const optionBox = document.createElement('div');
                optionBox.classList.add('p-2', 'border', 'rounded', 'flex', 'flex-col', 'items-center');

                const label = document.createElement('span');
                label.classList.add('font-bold', 'mb-1');
                label.textContent = String.fromCharCode(65 + index) + ".";

                const img = document.createElement('img');
                img.src = "https://cdn3.digialm.com" + url;
                img.alt = `Option ${label.textContent}`;
                img.classList.add('w-full');

                optionBox.appendChild(label);
                optionBox.appendChild(img);
                optionsContainer.appendChild(optionBox);
            }
        });

        mainContainer.appendChild(optionsContainer);
    }

    // Display user answer
    if (question.question_type === 'NAT') {
        mainContainer.innerHTML += `
            <p class="mt-4"><strong>Your Answer:</strong> ${question.given_answer || '<span class="text-gray-500">--</span>'}</p>
            <p><strong>Correct Range:</strong> ${correctAnswerKey[question.question_id]?.correct_ans || 'Not Available'}</p>
        `;
    } else if (question.question_type === 'MCQ' || question.question_type === 'MSQ') {
        const userAns = question.chosen_option || '--';
        const correctAns = correctAnswerKey[question.question_id]?.correct_ans || 'Not Available';

        mainContainer.innerHTML += `
            <p class="mt-4"><strong>Your Answer:</strong> ${userAns}</p>
            <p><strong>Correct Answer:</strong> ${correctAns}</p>
        `;
    }

    // Video
    const videoUrl = getVideoSolution(question.question_id);
    if (videoUrl) {
        mainContainer.innerHTML += `
            <div class="mt-6">
                <h3 class="font-semibold mb-2">Solution Video</h3>
                <video controls class="w-full max-w-xl">
                    <source src="${videoUrl}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        `;
    }

    return mainContainer;
}

// Run this when DOM is ready
if (q && q.length && correctAnswerKey) {
    displayNumbers();
    const first = q[0];
    if (first) {
        numberContainer.children[0].classList.add('active-number');
        dynamicContainer.appendChild(createQuestionDisplay(first));
    }
}




});
