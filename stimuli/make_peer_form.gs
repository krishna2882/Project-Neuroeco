// Paste into https://script.google.com (New project), then Run > createForm. Builds the peer-rating form.
const ITEMS = [
 [
  "M01",
  "This is the third time today I have been treated like an idiot, and I am completely fed up with all of it."
 ],
 [
  "M02",
  "Sorry for the slow reply. It has been a rough month, and lately there has not been much for me to look forward to."
 ],
 [
  "M03",
  "I was kept waiting for over an hour for this, and frankly the way this place treats people is a total insult."
 ],
 [
  "M04",
  "Today I did some laundry and answered a few emails. Later I need to buy groceries and drop off a library book."
 ],
 [
  "M05",
  "My grandmother passed away on Sunday. I never got to say goodbye, and I replay our last phone call in my head constantly."
 ],
 [
  "M06",
  "My team won the final in the last minute! I was jumping and shouting with my friends until well past midnight."
 ],
 [
  "M07",
  "I failed my exam again despite studying for weeks. I honestly do not know what I am doing wrong anymore."
 ],
 [
  "M08",
  "My exam results came out and I passed everything with top marks! I have been dancing around my kitchen all morning."
 ],
 [
  "M09",
  "Today was the anniversary of my father's death. I spent the morning at his grave, and I still cannot stop tearing up."
 ],
 [
  "M10",
  "I am using a laptop for this. The building has three floors, and my session is on the second floor near the stairs."
 ],
 [
  "M11",
  "My sister had her baby this morning, a healthy little girl. I have been smiling at photos of her all day long."
 ],
 [
  "M12",
  "Do not waste my time. I have dealt with nonsense all morning, and I am done putting up with people who play games."
 ],
 [
  "M13",
  "Whoever designed this has clearly never respected anyone's time. I am sick of these stupid hoops and these pointless rules."
 ],
 [
  "M14",
  "Honestly, I am sick of being messed around today. Nothing in this whole setup has gone right, and my patience is completely gone."
 ],
 [
  "M15",
  "Hi. I am filling this out between other tasks today, and the weather here is cloudy with some light wind this afternoon."
 ],
 [
  "M16",
  "Just got back from a beach trip with old friends. So much laughing, great food, and I slept like a baby."
 ],
 [
  "M17",
  "My dog died last night, and the house is so empty now. I find his old toys everywhere and cannot stop crying."
 ],
 [
  "M18",
  "Someone just scratched my car and drove off without a word. My jaw is clenched and I am slamming every door I pass."
 ],
 [
  "M19",
  "I just found out I got into my dream program! I have been grinning all morning and cannot stop calling everyone I know."
 ],
 [
  "M20",
  "I am typing this with my fists clenched. My boss just yelled at me over something that was not even my fault."
 ],
 [
  "M21",
  "I have been alone in my room all week. My friends stopped calling, and most nights I just stare at the ceiling."
 ],
 [
  "M22",
  "Sorry if I seem distracted. My partner moved out yesterday, and I have barely slept or eaten anything since then."
 ],
 [
  "M23",
  "My best friend moved abroad this week, and the city seems empty. I walk past our old cafe alone every evening."
 ],
 [
  "M24",
  "I am sitting at a desk near a window. I had tea earlier and will probably go to the library after this."
 ],
 [
  "M25",
  "This morning I made toast and checked the news. For the rest of the day I have some reading and a short meeting."
 ],
 [
  "M26",
  "Hello. I took the bus here this morning, and it took about twenty minutes. The room has a white table and chairs."
 ],
 [
  "M27",
  "I got engaged last night! I stare at the ring and laugh out loud every few minutes like a complete fool."
 ],
 [
  "M28",
  "What a wonderful day. I went for a long run by the lake, and everything about this afternoon seems so bright."
 ],
 [
  "M29",
  "Hi there. I read the instructions once and I think I understand the setup. It is a Tuesday afternoon here."
 ],
 [
  "M30",
  "Unbelievable. They changed the rules at the last minute again, and nobody even bothered to explain. This is absolutely ridiculous."
 ],
 [
  "M31",
  "The sun is out, my favourite song just came on, and I finally finished a project I had been dreading for months."
 ],
 [
  "M32",
  "I usually take the train to work. Today I walked instead because the station was closed for routine maintenance work."
 ]
];

function createForm() {
  const form = FormApp.create('Rating short messages');
  form.setDescription('You will read 32 short messages. For each, say which emotion the writer mainly expresses, how strongly, and whether it says what the writer will do to the reader. About 10 minutes. There are no right answers.');
  form.addTextItem().setTitle('Your initials').setRequired(true);
  ITEMS.forEach(([id, text], i) => {
    form.addPageBreakItem().setTitle(`Message ${i + 1} of ${ITEMS.length}`).setHelpText(`"${text}"`);
    form.addMultipleChoiceItem().setTitle(`[${id}] Which emotion does the writer mainly express?`)
      .setChoiceValues(['Neutral', 'Angry', 'Sad', 'Happy', 'Other']).setRequired(true);
    form.addScaleItem().setTitle(`[${id}] How strongly is that emotion expressed?`)
      .setBounds(1, 7).setLabels('Very weakly', 'Very strongly').setRequired(true);
    form.addMultipleChoiceItem().setTitle(`[${id}] Does the message say or imply what the writer will do to the reader (e.g. accept, reject, punish, reward)?`)
      .setChoiceValues(['No', 'Yes']).setRequired(true);
  });
  Logger.log('Share this link with raters: ' + form.getPublishedUrl());
  Logger.log('Edit the form here: ' + form.getEditUrl());
}
