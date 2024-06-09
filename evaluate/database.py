import sqlite3


class TextDatabase:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.current_position = 0
        # 创建一个新表用于存储文本数据，增加 word_count 字段
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                word_count INTEGER NOT NULL
            )
        """
        )
        self.connection.commit()

    def add_data(self, text):
        """
        添加文本到数据库，同时计算文本的词汇数量
        """
        word_count = len(text.split())  # 计算词汇数量
        self.cursor.execute(
            "INSERT INTO texts (content, word_count) VALUES (?, ?)", (text, word_count)
        )
        self.connection.commit()

    def get_data(self, min_words=None, max_words=None)->None|str:
        """
        从当前指针位置取出数据，可以指定最大和最小词汇数限制，指针指向取出文本的下一条数据
        """
        query = "SELECT content FROM texts WHERE id > ?"
        params = [self.current_position]

        if min_words is not None:
            query += " AND word_count >= ?"
            params.append(min_words)
        if max_words is not None:
            query += " AND word_count <= ?"
            params.append(max_words)

        query += " LIMIT ?"
        params.append(1)  # 限制为逐条取出

        self.cursor.execute(query, params)
        row = self.cursor.fetchone()
        if row:
            content = row[0]
            # 更新指针位置为当前取出数据的id
            self.current_position = self.cursor.execute(
                "SELECT id FROM texts WHERE content = ?", (content,)
            ).fetchone()[0]
            return content
        return None  # 如果没有数据，返回None

    def list_word_counts(self):
        """
        列举数据库中所有文本的词汇数量
        """
        self.cursor.execute("SELECT id, word_count FROM texts")
        return self.cursor.fetchall()

    def reset_cursor(self):
        """
        重置内置指针到初始位置
        """
        self.current_position = 0

    def close(self):
        """
        关闭数据库连接
        """
        self.connection.close()


# 加入数据[(1, 55), (2, 44), (3, 45), (4, 55), (5, 102), (6, 97), (7, 84), (8, 84), (9, 95), (10, 58)]
file_path = __file__
db_path = file_path.replace("database.py", "data.db")
DB = TextDatabase(db_path)


# DB.add_data(
#     """Life Is Not Perfect
# Go ahead with life as it is, with the bumps and pitfalls. However it is, give your best to every moment.
# Don't spend your time waiting for the perfect situation, something which is not very likely to come.
# Life is not perfect; the way you live can make it perfectly wonderful."""
# )
# DB.add_data(
#     """"Life Is Wonderful
# Face your past without regret.
# Handle your present with confidence.
# Prepare for the future without fear.
# Keep faith and drop the fear.
# Don't believe your doubts and never doubt your beliefs.
# Life is wonderful if you know how to live it."""
# )
# DB.add_data(
#     """"You Live Only Once
# Make the best of life's moments...
# What really matters at the end of the day is if you've made the best use of time,
# and done everything that you needed to do.
# Don't sit just there waiting, You only live once!"""
# )
# DB.add_data(
#     """Finish Each Day
# Finish each day and be done with it. You have done what you could.
# Some blunders and absurdities no doubt crept in; Forget them as soon as you can.
# Tomorrow is a new day; Begin it well and serenely,
# And with too high a spirit to be encumbered with your old nonsense."""
# )
# DB.add_data(
#     """The Power of Determination
# Determination is the key to success. 
# It is the force that enables a person to face challenges head on, 
# to dig deep when things get tough, and to keep going no matter what. Without determination,
# we would simply give up when faced with the slightest resistance. 
# But with it, we can overcome any obstacle and achieve any goal. 
# Determination is what makes us push beyond our limits, and it is what propels us forward in life. 
# It is the driving force behind all success stories, and it is the one quality that all successful people have in common. 
# """
# )
# DB.add_data(
#     """The Joy of Learning
# Learning is an adventure that never ends. 
# Curiosity drives us to explore new topics and master new skills. 
# It is the joy of uncovering something unknown that keeps our minds active and our hearts engaged. 
# In the vast expanse of knowledge, every discovery is a treasure. With each book we read, each experiment we conduct, and each conversation we engage in, we grow a little more. 
# Learning is not confined to classrooms or textbooks; it happens everywhere, every day. 
# So, let your curiosity lead you to new paths, new understandings, and endless possibilities."""
# )
# DB.add_data(
#     """Resilience in Adversity
# Life throws challenges our way that test our strength and determination. 
# It is not the absence of obstacles but how we respond to them that defines our character. 
# Resilience is the tool we use to bounce back from setbacks and move forward. 
# It's about maintaining a positive spirit and a steadfast heart in the face of difficulties. 
# Every challenge is an opportunity to prove our resilience and advance our capabilities. 
# By embracing adversity, we forge our path to success and happiness."""
# )
# DB.add_data(
#     """The Importance of Teamwork
# Success is seldom the result of one person’s efforts.
# Rather, it is the outcome of many hands and minds working together towards a common goal. 
# Teamwork harnesses the diverse strengths of its members, creating something greater than the sum of its parts. 
# Effective teams communicate openly, share responsibilities, and respect each other’s unique contributions. 
# When a team works in harmony, the impossible becomes possible. 
# Embrace teamwork, and see how collaboration can lift you higher than you could ever go alone."""
# )
# DB.add_data(
#     """Cultivating Creativity
# Creativity is not just for artists, writers, or musicians; 
# it's a valuable skill that can be nurtured in anyone. 
# It involves looking at problems from new angles, thinking outside the box, 
# and finding unique solutions. To cultivate creativity, seek out new experiences, 
# embrace curiosity, and be open to learning from failures. Remember, every great innovation starts with a creative idea. 
# So, challenge yourself to think differently, and you may be surprised at what you can achieve.
# Giving is not just about donations—it’s about making a positive impact. Volunteer, help others, and spread kindness."""
# )
# DB.add_data("""The Power of Patience
# Patience is a virtue that can transform your life. 
# It is about waiting for the right moment without frustration, 
# maintaining a calm demeanor in the face of delays, and enduring difficulties without complaint. 
# Patience allows us to make thoughtful decisions, avoid mistakes made in haste, and appreciate the journey as much as the destination.
# """)
# DB.add_data("""In the heart of the bustling city, amidst the concrete and noise, there lies a small oasis of greenery. This park, a refuge for weary souls, reminds us of the importance of preserving natural beauty in urban environments. It's a place where both nature and people find solace and rejuvenation.""")
# DB.add_data("As the sun sets over the coastal town, the sky turns a vibrant palette of orange and pink. Fishermen return with their catch, their boats gently bobbing in the calm sea, marking the end of another fruitful day.")
# DB.add_data("In the bustling market, aromas of fresh spices and colorful fruits mingle in the air. Vendors call out their wares with cheerful banter, inviting passersby to sample their offerings and enjoy the vibrant tapestry of local life.")
# DB.add_data("The ancient ruins stand as a testament to the grandeur of a bygone era. Weathered by time and the elements, they whisper stories of empires long past, inviting visitors to step back in time and marvel at the wonders of history.")
# DB.add_data("In the heart of the forest, a gentle stream winds its way through the trees, its waters glistening in the dappled sunlight. Birds sing in the branches above, their melodies blending with the rustling of leaves, creating a symphony of nature.")
# DB.add_data("The snow-capped peaks of the mountains rise majestically against the clear blue sky. A sense of peace and tranquility pervades the air, as the world below seems to fade away, leaving only the towering heights and the endless expanse of the heavens.")
# DB.add_data("In the quiet village, the sound of laughter and music fills the air as villagers gather for a festive celebration. The aroma of home-cooked meals wafts through the streets, inviting all to partake in the joyous occasion and share in the warmth of community.")
# DB.add_data("As the storm clouds gather on the horizon, the wind begins to howl and the rain falls in a steady rhythm. Thunder rumbles in the distance, echoing the power of nature as it unleashes its fury upon the land, reminding us of its awesome and untamed force.")
# DB.add_data("In the heart of the city, skyscrapers tower overhead, their glass facades reflecting the hustle and bustle of urban life below. Lights twinkle in the darkness, casting a warm glow over the streets, as the city comes alive with the energy of its inhabitants.")
# DB.add_data("The sun sets over the horizon, casting a golden light across the landscape. Shadows lengthen and colors deepen, as the world prepares to bid farewell to another day. The beauty of the moment is fleeting, but its memory will linger long after the sun has disappeared from view.")
# DB.add_data("Technology continues to advance at an astonishing rate, transforming every aspect of our lives. From smart homes to AI-driven healthcare, the future promises even greater integration of technology in daily living, making the impossible seem possible.")
# DB.add_data("As the world becomes increasingly interconnected, learning a second language has never been more important. It not only opens doors to new cultures and opportunities but also fosters understanding and collaboration among people of diverse backgrounds.")
# DB.add_data("In the midst of urban sprawl, community gardens emerge as vibrant sanctuaries where nature and community intertwine. These green spaces offer more than just a place for cultivating plants; they foster social interaction and connect people from diverse backgrounds. Residents, who might otherwise never cross paths, come together to plant, nurture, and harvest. The gardens become a canvas for communal creativity and a source of local pride. Amid the concrete jungle, they serve as crucial green lungs, improving air quality and providing a peaceful retreat from the city's hustle. Community gardens not only beautify neighborhoods but also strengthen the bonds of community, making the city feel more like home.")
# DB.add_data("A quaint bookstore tucked away in the city's historic quarter serves as a portal to the past. Every shelf, every book has a story, with first editions and rare manuscripts drawing in bibliophiles. The store's musty aroma, a blend of old paper and leather, evokes nostalgia. It's a place where time slows down, allowing visitors to explore the depths of literature and history. The owner, knowledgeable and passionate, guides each customer with personal recommendations, turning a simple visit into a journey through the annals of storytelling.")
# DB.add_data("The annual kite festival paints the sky with a mosaic of colors and shapes. Families and enthusiasts gather on the wide, open fields, releasing their kites into the breeze. The event is not just about flying kites but also celebrates creativity and engineering. Workshops teach the art of kite making, emphasizing the intersection of science and art. As the sun sets, LED-lit kites take flight in a luminous dance, creating a spectacle of light against the night sky, symbolizing unity and the joy of shared experiences.")
# DB.add_data("Urban beekeeping has gained momentum as an essential eco-friendly practice. Rooftops and balconies are transformed into thriving apiaries, where bees pollinate city gardens and parks. This initiative not only supports local ecosystems but also produces urban honey, a unique product that captures the essence of the city’s flora. Beekeepers, often volunteers, share knowledge and collaborate to maintain healthy colonies. Their efforts highlight the importance of sustainability and biodiversity in urban settings, proving that even small-scale interventions can have significant environmental impacts.")
# DB.add_data("Travel Blog Entry: Last summer, I experienced the unforgettable beauty of Italy's Amalfi Coast. The region is famous for its stunning ocean views, dramatic cliffs, and charming villages that seem to cascade down the rugged terrain. Every day brought new delights, from exploring ancient ruins steeped in history to tasting exquisite local dishes like seafood pasta, fresh from the Mediterranean Sea. The local Limoncello, made from sun-ripened lemons, was a refreshing treat. Each evening, the sun would set in a spectacular display of colors, casting a golden glow over the sea, transforming the view into a living painting that captivated my heart and soul.")
# DB.add_data("Technology Review: The latest smartphone released by TechGiant is a powerhouse of innovation, setting a new benchmark in the mobile technology industry. With its cutting-edge processor, the phone delivers exceptional speed and efficiency, making multitasking seamless. The advanced camera system offers unmatched photo and video quality, even in low light conditions. The device also features a high-resolution display that brings colors and details to life, perfect for media enthusiasts. Additionally, its robust battery life ensures that users can enjoy a full day's worth of activity without the need for recharging, making it an ideal choice for professionals and tech enthusiasts who demand reliability and performance.")
# DB.add_data("Health and Wellness Advice: Adopting a healthy lifestyle is essential for maintaining long-term well-being. This includes eating a balanced diet rich in vitamins and minerals, engaging in regular physical activity tailored to your personal needs, and ensuring adequate rest and recovery through quality sleep. Additionally, managing stress through mindfulness practices such as meditation, yoga, or deep breathing exercises can significantly improve mental and emotional health. By making these practices a regular part of your routine, you can enhance your overall health, increase your energy levels, and reduce the risk of chronic diseases.")
# DB.add_data("Historical Anecdote: During the Victorian era, fashion was a complex expression of social status and identity, with women's clothing featuring voluminous skirts, tight corsets, and an array of accessories that indicated one's social standing. The fabrics used were often rich and ornate, including silk, velvet, and lace, embellished with intricate embroidery. Men's attire was equally structured, with tailored suits and top hats symbolizing respectability and success. This period also saw significant cultural developments, including the rise of the arts and literature, which were influenced by and reflected in the fashion trends of the time.")
# DB.add_data("Environmental Awareness: Global warming is an urgent issue that requires immediate and sustained action from all sectors of society. Individuals can contribute by adopting more sustainable practices like reducing waste, conserving water, and using public transport or carpooling to reduce carbon emissions. Additionally, supporting local and global environmental initiatives can lead to significant positive changes. By making informed choices about the products we use and the energy we consume, we can collectively make a difference in combating climate change and protecting our planet for future generations.")
# DB.add_data("Recipe Blog: This blueberry cheesecake recipe is not only delicious but also simple to make. Start with a base of crushed graham crackers mixed with melted butter to form a solid crust. Blend cream cheese, sugar, eggs, and vanilla extract together until smooth for the filling, then pour it over the crust. Bake in a preheated oven until the center is just set. Top the cooled cheesecake with a layer of fresh blueberries and a sprinkle of powdered sugar for added sweetness. This dessert is perfect for any occasion, combining the creamy texture of the cheesecake with the fresh, tangy flavor of blueberries.")
# print(DB.list_word_counts())