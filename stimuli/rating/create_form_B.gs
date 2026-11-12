/**
 * Project Neuroeco - creates rating Form B (anonymous, ~5 minutes). Form A has its own script.
 *
 * HOW TO USE (about 2 minutes):
 *  1. Go to https://script.google.com  ->  "New project".
 *  2. Delete the sample code, paste this whole file, click Save.
 *  3. At the top choose the function "createForm" and click Run. Approve the permission prompt
 *     (it only creates one form in your own Google Drive).
 *  4. Open "Execution log": it prints the links. Send the Form B link to ~8 people (the other form goes to ~8 different people).
 *
 * The forms do NOT collect names or emails. Nothing about the study's purpose or AI is shown to raters.
 */
var PAGES = [
 {
  "page": 1,
  "items": [
   {
    "n": 1,
    "text": "I got engaged last night! I stare at the ring and laugh out loud every few minutes like a complete fool."
   },
   {
    "n": 2,
    "text": "I have been alone in my room all week. My friends stopped calling, and most nights I just stare at the ceiling."
   },
   {
    "n": 3,
    "text": "Ugh. I am stomping around and snapping at everything. My blood is up, my face is red, and I cannot calm down."
   },
   {
    "n": 4,
    "text": "There is so much warmth in my chest right now. I have been laughing and singing to myself since I woke up."
   },
   {
    "n": 5,
    "text": "Do not waste my time. I have dealt with nonsense all morning, and I am done putting up with people who play games."
   },
   {
    "n": 6,
    "text": "The sun is out, my favourite song just came on, and I finally finished a project I had been dreading for months."
   }
  ]
 },
 {
  "page": 2,
  "items": [
   {
    "n": 1,
    "text": "My team won the final in the last minute! I was jumping and shouting with my friends until well past midnight."
   },
   {
    "n": 2,
    "text": "My eyes are puffy from crying and my chest aches. Everything is grey right now, and I just want to curl up in bed."
   },
   {
    "n": 3,
    "text": "I am typing at a steady pace. The chair is comfortable enough, and there is some background noise from the corridor outside."
   },
   {
    "n": 4,
    "text": "I feel heavy and slow today. I have been staring at the wall for hours, and nothing seems worth the effort anymore."
   },
   {
    "n": 5,
    "text": "I am sitting at a desk and typing this on a laptop. The room is quiet, and the light is ordinary. Nothing much else."
   }
  ]
 },
 {
  "page": 3,
  "items": [
   {
    "n": 1,
    "text": "I have been crying on and off all afternoon. My body is drained, and I cannot remember the last time anything seemed good."
   },
   {
    "n": 2,
    "text": "I woke up full of energy and bursting with good cheer. I am practically dancing around the room right now."
   },
   {
    "n": 3,
    "text": "I am in a plain room with a table and two chairs. The window is closed, and the temperature is normal."
   },
   {
    "n": 4,
    "text": "I am grinning from ear to ear today. Everything seems light and bright, and I cannot stop humming my favourite tunes."
   },
   {
    "n": 5,
    "text": "I am using a laptop for this. The building has three floors, and my session is on the second floor near the stairs."
   }
  ]
 },
 {
  "page": 4,
  "items": [
   {
    "n": 1,
    "text": "I am so fed up right now that my hands are shaking. Nothing is going right, and I am sick of all of it."
   },
   {
    "n": 2,
    "text": "I feel on top of the world right now. Music is playing in my head, and I have a huge silly grin on my face."
   },
   {
    "n": 3,
    "text": "I am gripping this desk so hard my knuckles are white. I could scream at the next tiny thing that goes wrong."
   },
   {
    "n": 4,
    "text": "My whole body is tense and hot. I have been slamming drawers and glaring at the wall for the last hour."
   },
   {
    "n": 5,
    "text": "There is a lump in my throat that will not go away. I sit in silence most evenings, and tears come without warning."
   }
  ]
 },
 {
  "page": 5,
  "items": [
   {
    "n": 1,
    "text": "I am logged in and ready. The keyboard works, the screen is bright enough, and the room is at a normal temperature."
   },
   {
    "n": 2,
    "text": "My dog died last night, and the house is so empty now. I find his old toys everywhere and cannot stop crying."
   },
   {
    "n": 3,
    "text": "I was kept waiting for over an hour for this, and frankly the way this place treats people is a total insult."
   },
   {
    "n": 4,
    "text": "Today was the anniversary of my father's death. I spent the morning at his grave, and I still cannot stop tearing up."
   },
   {
    "n": 5,
    "text": "Hello. I took the bus here this morning, and it took about twenty minutes. The room has a white table and chairs."
   }
  ]
 }
];

var INTRO =
  'Hi! This takes about 5 minutes. It is completely anonymous: we do not collect your name or email.\n\n' +
  'THE SITUATION\n' +
  'Imagine a simple money game between two people who never meet. For example: one person has Rs 100 and ' +
  'decides how much of it to give to the other person. Just before deciding, they receive a short message ' +
  'from the other person.\n\n' +
  'WHAT YOU DO\n' +
  'You will read short messages like that, about 5 per page. For each message, answer two quick questions:\n' +
  '  1. What feeling does the writer show?\n' +
  '  2. If you were the one deciding, would this message make you give the writer less money, about the same, or more?\n\n' +
  'There are no right or wrong answers. Go with your first feeling - most people take a few seconds per message.';

function buildForm_(name, pages) {
  var form = FormApp.create('Quick survey: how do these short messages sound? (' + name + ', about 5 minutes)');
  form.setDescription(INTRO);
  form.setCollectEmail(false);
  try { form.setRequireLogin(false); } catch (e) {}   // only matters for school/work Google accounts
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Thank you so much! Your answers have been saved.');

  pages.forEach(function (pg, i) {
    if (i > 0) form.addPageBreakItem().setTitle('Page ' + pg.page + ' of ' + pages.length);
    var rows = pg.items.map(function (it) { return it.n + '. "' + it.text + '"'; });
    form.addSectionHeaderItem()
      .setTitle('Page ' + pg.page + ': messages from the other person')
      .setHelpText('Imagine each message was sent to you just before you decide how much money to give the writer. ' +
                   'Each message is from a different person.');
    form.addGridItem()
      .setTitle('What feeling does the writer show? (page ' + pg.page + ')')
      .setHelpText('Pick the one that fits best. "Neutral" = no particular feeling.')
      .setRows(rows)
      .setColumns(['Neutral', 'Angry', 'Sad', 'Happy', 'Something else'])
      .setRequired(true);
    form.addGridItem()
      .setTitle('Would this message make you give the writer less money, about the same, or more? (page ' + pg.page + ')')
      .setHelpText('Compared with getting no message at all.')
      .setRows(rows)
      .setColumns(['Less', 'About the same', 'More'])
      .setRequired(true);
    var choices = pg.items.map(function (it) { return 'Message ' + it.n; });
    choices.push('None of them');
    form.addCheckboxItem()
      .setTitle('Does any message on this page sound like a threat or a promise to you? (page ' + pg.page + ')')
      .setHelpText('For example: "I will refuse anything unfair" or "If you are kind, I will pay you back". ' +
                   'Most messages are neither - if so, just tick "None of them".')
      .setChoiceValues(choices)
      .setRequired(true);
  });
  return form;
}

function createForm() {
  var form = buildForm_('Form B', PAGES);
  Logger.log('FORM B - link to send to raters: ' + form.getPublishedUrl());
  Logger.log('FORM B - edit link (keep for yourself): ' + form.getEditUrl());
}
