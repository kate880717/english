# -*- coding: utf-8 -*-
import re

file_path = r"c:\Users\kjhis\OneDrive\바탕 화면\새 폴더 (2)\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_block = '''        function StageWriting({ onComplete }) {
            const [paragraph, setParagraph] = useState('');
            const [isEvaluating, setIsEvaluating] = useState(false);
            const [result, setResult] = useState(null);

            const GRADE_CONFIG = {
                '잘함':    { color: 'bg-emerald-50 border-emerald-300', badge: 'bg-emerald-500', icon: '🌟' },
                '보통':    { color: 'bg-amber-50 border-amber-300',   badge: 'bg-amber-500',   icon: '👍' },
                '노력요함': { color: 'bg-rose-50 border-rose-300',     badge: 'bg-rose-500',     icon: '💪' },
            };

            const evaluate = async () => {
                if (!paragraph.trim() || paragraph.trim().length < 10) return;
                setIsEvaluating(true);
                setResult(null);
                try {
                    const prompt = `다음 규칙에 따라 학생이 작성한 문단을 평가해주세요.

[기본 평가 사항]
1. 중심 문장: 문단의 처음이나 마지막에 위치하는지, 모든 뒷받침 문장을 포괄하는지 확인. 너무 단순하거나 짧으면 수정 방법 안내.
2. 뒷받침 문장: 중심 문장을 잘 뒷받침하는지, 문단에 어울리지 않는 문장이 있는지 확인.
3. 맞춤법: 틀린 맞춤법이 있으면 정확한 표기와 함께 설명.

[평가 기준]
- 잘함: 문장 4~5개 이상, 중심+뒷받침 조건 잘 갖춤, 짜임새 있고 생각이 효과적으로 드러남
- 보통: 조건 일부 갖춤, 부족한 부분 1~2가지, 구조는 지켜짐, 표현이 다소 서툴지만 내용은 적합
- 노력요함: 중심/뒷받침 부분적, 내용 연결 매끄럽지 않음, 어울리지 않는 문장 포함, 맞춤법 3~4개 이상 틀림

[평가 형식]
기본 평가 사항에 대한 내용을 한 문단 분량으로 정리하고, 마지막에는 "그래서 친구의 평가 결과는 ~야"로 마무리.

JSON으로만 응답 (마크다운 없이):
{
  "grade": "잘함" | "보통" | "노력요함",
  "summary": "한 문단 분량의 평가 내용 (학생에게 친근하게, 구체적으로)",
  "closing": "그래서 친구의 평가 결과는 ~야"
}

[학생 문단]
${paragraph}`;

                    const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
                        method: 'POST', headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
                    });
                    const data = await res.json();
                    const parsed = JSON.parse(data.candidates[0].content.parts[0].text.replace(/```json|```/g, '').trim());
                    setResult(parsed);
                } catch (e) {
                    setResult({ grade: '보통', summary: '평가 중 오류가 발생했어요. 다시 시도해보세요!', closing: '그래서 친구의 평가 결과는 보통이야' });
                } finally {
                    setIsEvaluating(false);
                }
            };

            const cfg = result ? (GRADE_CONFIG[result.grade] || GRADE_CONFIG['보통']) : null;

            return (
                <div className="flex flex-col items-center justify-center w-full animate-fade-in py-8">
                    <div className="bg-white rounded-[3rem] p-12 shadow-neubrutalism shadow-rose-100 w-full max-w-4xl border-4 border-slate-900 relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-full h-4 bg-gradient-to-r from-rose-400 to-pink-400 border-b-4 border-slate-900"></div>

                        <div className="mb-6 flex justify-between items-center">
                            <span className="bg-rose-50 text-rose-600 px-5 py-2 rounded-full text-sm font-bold tracking-wide border-2 border-rose-200">STEP 5. 문단 평가</span>
                            {result && <button onClick={() => { setResult(null); setParagraph(''); }} className="text-slate-400 hover:text-rose-500 font-bold text-sm flex items-center gap-1">다시 쓰기 <RefreshCw size={14} /></button>}
                        </div>

                        <div className="rounded-2xl border-2 p-4 mt-2 mb-4 bg-rose-50 border-rose-200 text-rose-800">
                            <p className="text-xs font-black uppercase tracking-widest mb-2 opacity-60">이 단계에서 나는...</p>
                            <ul className="space-y-1.5">
                                <li className="flex items-start gap-2 text-sm font-bold"><span className="mt-0.5 shrink-0">💡</span>내가 쓴 문단에 중심 문장과 뒷받침 문장이 잘 연결되어 있나요?</li>
                                <li className="flex items-start gap-2 text-sm font-bold"><span className="mt-0.5 shrink-0">💡</span>내가 쓴 내용이 주제를 잘 담고 있나요?</li>
                                <li className="flex items-start gap-2 text-sm font-bold"><span className="mt-0.5 shrink-0">💡</span>AI 도구로 내 글을 평가받으면 어떤 점을 고칠 수 있는지 알 수 있어요!</li>
                            </ul>
                        </div>

                        {!result ? (
                            <div className="mt-6">
                                <h2 className="text-3xl font-black text-slate-800 mb-2 text-center">내 문단 평가받기</h2>
                                <p className="text-slate-500 font-bold text-center mb-6">아래에 쓴 문단을 입력하면 AI가 평가해줘요! 한국어로 써도 돼요.</p>
                                <div className="relative">
                                    <textarea
                                        value={paragraph}
                                        onChange={e => setParagraph(e.target.value)}
                                        placeholder="여기에 내가 쓴 문단을 입력하세요..."
                                        className="w-full h-52 p-6 bg-slate-50 rounded-3xl border-4 border-slate-200 focus:border-rose-400 outline-none text-lg font-medium text-slate-700 resize-none leading-relaxed custom-scrollbar"
                                    />
                                    <div className="absolute bottom-4 right-5 text-xs font-bold text-slate-300">{paragraph.length}자</div>
                                </div>
                                <button
                                    onClick={evaluate}
                                    disabled={isEvaluating || paragraph.trim().length < 10}
                                    className="mt-6 w-full bg-rose-500 text-white py-5 rounded-3xl font-black text-2xl shadow-neubrutalism hover:bg-rose-600 flex items-center justify-center gap-3 border-4 border-slate-900 disabled:opacity-50 transition-all hover:scale-[1.01]"
                                >
                                    {isEvaluating ? <><Loader2 size={28} className="animate-spin" /> AI가 평가 중...</> : <>평가 받기 <Send size={28} /></>}
                                </button>
                            </div>
                        ) : (
                            <div className="mt-6 animate-fade-in-up">
                                <div className={`rounded-3xl border-4 p-8 mb-6 ${cfg.color}`}>
                                    <div className="flex items-center justify-center gap-4 mb-4">
                                        <span className="text-5xl">{cfg.icon}</span>
                                        <span className={`px-8 py-3 rounded-full text-white font-black text-3xl border-4 border-slate-900 shadow-neubrutalism ${cfg.badge}`}>
                                            {result.grade}
                                        </span>
                                    </div>
                                    <p className="text-slate-700 font-bold text-base leading-relaxed text-left bg-white/60 rounded-2xl p-5 mb-4">
                                        {result.summary}
                                    </p>
                                    <div className={`text-center font-black text-xl p-4 rounded-2xl bg-white/80 border-2 ${cfg.color}`}>
                                        "{result.closing}"
                                    </div>
                                </div>
                                <div className="flex gap-4">
                                    <button onClick={() => setResult(null)} className="flex-1 bg-white border-4 border-slate-900 text-slate-700 py-4 rounded-2xl font-bold text-lg shadow-neubrutalism hover:bg-slate-50 flex items-center justify-center gap-2">
                                        <RefreshCw size={20} /> 다시 평가
                                    </button>
                                    <button onClick={onComplete} className="flex-1 bg-slate-800 text-white py-4 rounded-2xl font-bold text-lg shadow-neubrutalism hover:bg-slate-700 flex items-center justify-center gap-2 border-4 border-slate-900">
                                        Dream Card 만들기 <ArrowRight size={20} />
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            );
        }'''

# StageWriting 함수 전체를 찾아서 교체 (function StageWriting부터 다음 function 선언 전까지)
pattern = r'        function StageWriting\(\{ onComplete \}\) \{.*?\n        \}'
match = re.search(pattern, content, re.DOTALL)
if match:
    print(f"Found StageWriting at: {match.start()} - {match.end()}")
    content = content[:match.start()] + new_block + content[match.end():]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: StageWriting replaced!")
else:
    print("ERROR: StageWriting function not found!")
    # 디버그: 처음 몇 글자 확인
    idx = content.find('function StageWriting')
    if idx >= 0:
        print(f"Found at index {idx}: {repr(content[idx:idx+100])}")
    else:
        print("StageWriting not found at all")
