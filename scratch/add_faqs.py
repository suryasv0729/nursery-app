import os

html_file = 'c:\\Users\\admin\\Desktop\\Kanna\\nursery_app\\templates\\planting_tips.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

def inject_faq(content, identifier, title, faqs):
    faq_html = f'''
                <div class="mt-8 bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6 border-b border-gray-100 pb-4">{title}</h2>
                    <div class="space-y-4">'''
    
    for q, a in faqs:
        faq_html += f'''
                        <details class="group border border-gray-200 rounded-xl bg-gray-50 p-4 [&_summary::-webkit-details-marker]:hidden cursor-pointer shadow-sm hover:shadow-md transition">
                            <summary class="flex justify-between items-center font-medium cursor-pointer list-none text-md text-gray-900">
                                <span>{q}</span>
                                <span class="transition group-open:rotate-180"><i class="fa-solid fa-chevron-down text-green-600"></i></span>
                            </summary>
                            <div class="text-gray-600 mt-4 leading-relaxed bg-white p-4 rounded-lg border border-gray-100 text-sm">
                                {a}
                            </div>
                        </details>'''
        
    faq_html += '''
                    </div>
                </div>
            </div>'''
            
    # Find the end of the specified tab and inject
    target_str = f"</div>\n                </div>\n            </div>\n\n            <!-- {identifier} -->"
    replacement_str = f"</div>\n                </div>\n{faq_html}\n\n            <!-- {identifier} -->"
    
    if identifier == "Pots":
        target_str = "</div>\n                </div>\n            </div>\n\n        </div>\n    </div>\n</section>"
        replacement_str = f"</div>\n                </div>\n{faq_html}\n\n        </div>\n    </div>\n</section>"
        
    return content.replace(target_str, replacement_str)

faqs_indoor = [
    ("How often should I water my indoor plants?", "Generally, wait until the top 1-2 inches of soil are dry. Overwatering is a common mistake; it's better to underwater slightly than to keep the soil constantly soggy."),
    ("Why are the leaves on my indoor plant turning yellow?", "Yellow leaves can be a sign of overwatering, underwatering, poor drainage, or a lack of sunlight. Check the soil moisture first to determine if watering is the issue."),
    ("Can I use regular outdoor soil for indoor plants?", "No, outdoor soil is usually too heavy and doesn't drain well enough for indoor pots. It may also contain pests or diseases. Always use a high-quality indoor potting mix."),
    ("Do indoor plants need direct sunlight?", "Most popular indoor plants prefer bright, indirect light rather than direct sunlight, which can scorch their leaves.")
]

faqs_outdoor = [
    ("When is the best time to plant outdoor flowers or shrubs?", "Spring and early autumn are generally the best times to plant, as the weather is milder, reducing transplant shock and allowing roots to establish before extreme temperatures."),
    ("How much mulch should I apply around my outdoor plants?", "Apply about 2 to 3 inches of mulch around the base of your plants. Make sure to keep the mulch a few inches away from the plant stem to prevent rot."),
    ("How do I protect outdoor plants from frost?", "Cover plants with a frost cloth, bed sheets, or burlap before sunset. Watering the soil beforehand can also help trap heat."),
    ("How often should I fertilize my outdoor garden?", "This depends on the plant, but typically, applying a slow-release granular fertilizer in the spring and optionally in mid-summer is sufficient for most outdoor gardens.")
]

faqs_succulents = [
    ("How do I know if I'm overwatering my succulents?", "Overwatered succulents will have mushy, translucent, or yellow leaves that easily fall off. If this happens, stop watering and check the roots for rot."),
    ("Why is my succulent stretching and getting tall?", "This is called etiolation, and it happens when the succulent isn't getting enough light. Move it to a brighter spot to encourage compact growth (but introduce it gradually to avoid sunburn)."),
    ("What kind of soil is best for succulents?", "Succulents need fast-draining soil. Use a specialized cactus/succulent mix, or make your own by mixing regular potting soil with plenty of perlite, pumice, or coarse sand."),
    ("Can succulents survive in rooms with no natural light?", "Most succulents require bright, indirect or direct sunlight. Without natural light, you will need a strong grow light; otherwise, they will stretch and eventually decline.")
]

faqs_seeds = [
    ("How deep should I plant my seeds?", "A general rule of thumb is to plant a seed twice as deep as its diameter. Very tiny seeds often just need to be pressed into the surface of the soil, as they need light to germinate."),
    ("Why are my seedlings falling over and dying?", "This is likely 'damping off', a fungal disease caused by overly wet soil and poor airflow. Ensure good drainage, avoid overwatering, and provide gentle air circulation with a small fan."),
    ("Do I need a heat mat to start seeds indoors?", "While not strictly necessary for all seeds, a heat mat significantly speeds up germination for heat-loving plants like tomatoes, peppers, and eggplants."),
    ("How long does it usually take for seeds to germinate?", "Germination times vary widely by plant type. Rapid growers like radishes might sprout in 3-5 days, while others like peppers can take 1-3 weeks. Check the seed packet for specific times.")
]

faqs_pesticides = [
    ("How often should I apply organic pesticides?", "Usually, every 7 to 14 days or after heavy rainfall. Always read the specific product label, as application frequency can vary based on the pest severity and product strength."),
    ("Do organic pesticides harm bees or ladybugs?", "While safer than synthetic alternatives, some organic pesticides (like pyrethrin or even high concentrations of neem oil) can harm beneficial insects if sprayed directly on them. Apply at dawn or dusk when bees are less active."),
    ("Can I use neem oil on all types of plants?", "Most plants tolerate neem oil well, but it can burn foliage on some sensitive plants or if applied during the heat of the day. Always do a patch test first."),
    ("Are organic pesticides safe for pets and children?", "They are generally safer than chemical pesticides but can still be irritants or toxic if ingested in large quantities. Store them safely and keep pets and children away right after application until it dries.")
]

faqs_pots = [
    ("Does my pot really need a drainage hole?", "Yes! A drainage hole is essential to prevent water from pooling at the bottom, which leads to root rot. If you have a decorative pot without a hole, use it as a 'cachepot' and keep the plant in a plastic nursery pot inside it."),
    ("How do I clean a terracotta pot before reusing it?", "Scrub off loose dirt, then soak it in a solution of 1 part white vinegar to 4 parts water for a few hours to dissolve mineral buildup. Rinse thoroughly and let dry."),
    ("Which is better for my plant: a plastic or terracotta pot?", "It depends on the plant. Terracotta breathes and wicks moisture away, making it great for succulents or overwaterers. Plastic retains moisture better, making it ideal for ferns or tropicals."),
    ("When should I upgrade my plant to a larger pot?", "Repot when roots start growing out of the drainage holes, pushing the plant up, or if water runs straight through the soil without soaking in. Only size up 1-2 inches in diameter at a time.")
]


content = inject_faq(content, "Outdoor Tab", "Indoor Plants FAQ", faqs_indoor)
content = inject_faq(content, "Succulents Tab", "Outdoor Wonders FAQ", faqs_outdoor)
content = inject_faq(content, "Seeds Tab", "Succulents FAQ", faqs_succulents)
content = inject_faq(content, "Pesticides Tab", "Seeds FAQ", faqs_seeds)
content = inject_faq(content, "Pots Tab", "Organic Pesticides FAQ", faqs_pesticides)
content = inject_faq(content, "Pots", "Pots & Planters FAQ", faqs_pots)

# Let's remove the global FAQ section
start_marker = "<!-- Additional Care Guidelines FAQ -->"
end_marker = "</section>"

start_idx = content.find(start_marker)
if start_idx != -1:
    end_idx = content.find(end_marker, start_idx)
    if end_idx != -1:
        # also remove trailing whitespace if possible
        content = content[:start_idx] + content[end_idx + len(end_marker):]

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
    
print("Updated FAQs.")
