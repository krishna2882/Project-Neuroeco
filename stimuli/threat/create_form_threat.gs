/**
 * Project Neuroeco, extension 3 - ONE anonymous rating form, 20 messages (~5 minutes). Send to ~8-10 people
 * who did not do the 13 Nov form if possible. Same steps as before: script.google.com -> New project ->
 * paste -> Save -> run createForm -> Execution log shows the links. No names or emails are collected.
 */
var PAGES = [
 {
  "page": 1,
  "items": [
   {
    "n": 1,
    "text": "The repair man promised to come on Monday, then Tuesday, and still has not shown up. I am livid about being messed around like this."
   },
   {
    "n": 2,
    "text": "There is a lump in my throat that will not go away. I sit in silence most evenings, and tears come without warning."
   },
   {
    "n": 3,
    "text": "I am grinning from ear to ear today. Everything seems light and bright, and I cannot stop humming my favourite tunes."
   },
   {
    "n": 4,
    "text": "Lately I move through each day like a ghost. Nothing brings any spark, and the evenings are the hardest part of all."
   },
   {
    "n": 5,
    "text": "I feel heavy and slow today. I have been staring at the wall for hours, and nothing seems worth the effort anymore."
   }
  ]
 },
 {
  "page": 2,
  "items": [
   {
    "n": 1,
    "text": "The train was cancelled again this morning without a single announcement. It is outrageous how badly that line is run, week after week."
   },
   {
    "n": 2,
    "text": "I am logged in and ready. The keyboard works, the screen is bright enough, and the room is at a normal temperature."
   },
   {
    "n": 3,
    "text": "I am gripping this desk so hard my knuckles are white. I could scream at the next tiny thing that goes wrong."
   },
   {
    "n": 4,
    "text": "The website crashed right as I submitted my form and wiped everything I had typed. That kind of careless design infuriates me."
   },
   {
    "n": 5,
    "text": "There is so much warmth in my chest right now. I have been laughing and singing to myself since I woke up."
   }
  ]
 },
 {
  "page": 3,
  "items": [
   {
    "n": 1,
    "text": "It is an ordinary afternoon here. I am reading the instructions on the screen and will answer once I have read them."
   },
   {
    "n": 2,
    "text": "A delivery company lost my parcel and then claimed it was my fault. I am still seething about how they handled the whole thing."
   },
   {
    "n": 3,
    "text": "My neighbour's car alarm went off for two hours last night and nobody did anything. I still cannot believe how inconsiderate that was."
   },
   {
    "n": 4,
    "text": "I am bouncing on my toes like a child. The sky looks brighter than usual, and I cannot wipe this smile off my face."
   },
   {
    "n": 5,
    "text": "There is a pounding in my temples and my teeth are grinding. I have no tolerance left for anything or anyone today."
   }
  ]
 },
 {
  "page": 4,
  "items": [
   {
    "n": 1,
    "text": "The council dug up our street again and then left it like that for weeks. It makes my blood boil just thinking about it."
   },
   {
    "n": 2,
    "text": "This is a regular weekday for me. I am seated, the screen is on, and there is a pen and notebook beside me."
   },
   {
    "n": 3,
    "text": "My flatmate used up all the hot water again without asking. It has happened every day this week, and it drives me up the wall."
   },
   {
    "n": 4,
    "text": "Someone pushed in front of the whole queue at the post office this morning, and the staff just let it happen. Outrageous."
   },
   {
    "n": 5,
    "text": "Honestly, I am boiling inside right now. My heart is pounding, my shoulders are tight, and I want to slam a door."
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
  var form = FormApp.create('Quick survey: how do these short messages sound? (about 5 minutes)');
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
  var form = buildForm_('All messages', PAGES);
  Logger.log('Link to send to raters: ' + form.getPublishedUrl());
  Logger.log('Edit link (keep for yourself): ' + form.getEditUrl());
}
